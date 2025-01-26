from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from projects.models import Project
from costs.models import CostCategory, Cost
from schedules.models import Schedule
from materials.models import MaterialCategory, Material

# 既存のデータをクリア
Project.objects.all().delete()
CostCategory.objects.all().delete()
Cost.objects.all().delete()
Schedule.objects.all().delete()
MaterialCategory.objects.all().delete()
Material.objects.all().delete()

# 既存の管理者ユーザーを取得
admin_user = User.objects.get(username="admin")

# 現場監督ユーザーの作成（既存の場合は取得、存在しない場合は作成）
site_manager1, _ = User.objects.get_or_create(
    username="yamada",
    defaults={
        "email": "yamada@example.com",
        "first_name": "太郎",
        "last_name": "山田",
    },
)
site_manager1.set_password("yamada123")
site_manager1.save()

site_manager2, _ = User.objects.get_or_create(
    username="tanaka",
    defaults={
        "email": "tanaka@example.com",
        "first_name": "花子",
        "last_name": "田中",
    },
)
site_manager2.set_password("tanaka123")
site_manager2.save()

# プロジェクトの作成
today = timezone.now().date()

projects = [
    Project.objects.create(
        name="○○マンション新築工事",
        location="東京都渋谷区○○1-1-1",
        start_date=today,
        end_date=today + timedelta(days=365),
        description="地上10階建て、総戸数50戸の分譲マンション新築工事",
        manager=site_manager1,
    ),
    Project.objects.create(
        name="△△小学校改修工事",
        location="東京都新宿区△△2-2-2",
        start_date=today + timedelta(days=30),
        end_date=today + timedelta(days=180),
        description="築40年の小学校校舎の耐震補強および内装改修工事",
        manager=site_manager2,
    ),
    Project.objects.create(
        name="□□オフィスビル建設工事",
        location="東京都千代田区□□3-3-3",
        start_date=today + timedelta(days=60),
        end_date=today + timedelta(days=540),
        description="地上20階建て、オフィスビル新築工事",
        manager=site_manager1,
    ),
]

# 原価カテゴリの作成
cost_categories = [
    CostCategory.objects.create(
        name="資材費", description="建設資材、設備機器等の購入費用"
    ),
    CostCategory.objects.create(name="労務費", description="作業員、技術者等の人件費"),
    CostCategory.objects.create(name="外注費", description="専門工事業者への外注費用"),
    CostCategory.objects.create(name="経費", description="現場運営費、仮設費用等"),
]

# 原価データの作成
for project in projects:
    # 資材費
    Cost.objects.create(
        project=project,
        category=cost_categories[0],
        item_name="鉄骨材料",
        planned_amount=50000000,
        actual_amount=48000000,
        payment_status="paid",
        payment_date=today - timedelta(days=30),
        invoice_number="INV-001",
    )

    # 労務費
    Cost.objects.create(
        project=project,
        category=cost_categories[1],
        item_name="型枠工事人件費",
        planned_amount=30000000,
        actual_amount=32000000,
        payment_status="partially_paid",
        payment_date=today,
        invoice_number="INV-002",
    )

    # 外注費
    Cost.objects.create(
        project=project,
        category=cost_categories[2],
        item_name="電気設備工事",
        planned_amount=40000000,
        actual_amount=None,
        payment_status="unpaid",
        payment_date=None,
        invoice_number="",
    )

    # 経費
    Cost.objects.create(
        project=project,
        category=cost_categories[3],
        item_name="仮設事務所費用",
        planned_amount=5000000,
        actual_amount=4800000,
        payment_status="paid",
        payment_date=today - timedelta(days=60),
        invoice_number="INV-003",
    )

# スケジュールの作成
for project in projects:
    Schedule.objects.create(
        project=project,
        task_name="基礎工事",
        planned_start_date=project.start_date,
        planned_end_date=project.start_date + timedelta(days=60),
        actual_start_date=project.start_date,
        actual_end_date=None,
        status="in_progress",
        progress=30,
        assigned_to=project.manager,
    )

    Schedule.objects.create(
        project=project,
        task_name="躯体工事",
        planned_start_date=project.start_date + timedelta(days=61),
        planned_end_date=project.start_date + timedelta(days=180),
        actual_start_date=None,
        actual_end_date=None,
        status="not_started",
        progress=0,
        assigned_to=project.manager,
    )

    Schedule.objects.create(
        project=project,
        task_name="設備工事",
        planned_start_date=project.start_date + timedelta(days=120),
        planned_end_date=project.start_date + timedelta(days=240),
        actual_start_date=None,
        actual_end_date=None,
        status="not_started",
        progress=0,
        assigned_to=(
            site_manager2 if project.manager == site_manager1 else site_manager1
        ),
    )

# 資材カテゴリの作成
material_categories = [
    MaterialCategory.objects.create(name="建材", description="建築資材全般"),
    MaterialCategory.objects.create(name="設備機器", description="電気・機械設備機器"),
    MaterialCategory.objects.create(name="工具", description="工具類"),
]

# 資材データの作成
materials = [
    Material.objects.create(
        category=material_categories[0],
        name="コンクリート（普通）",
        code="M001",
        specification="24-18-20",
        unit="m3",
        unit_price=15000,
        current_stock=100,
        minimum_stock=50,
    ),
    Material.objects.create(
        category=material_categories[0],
        name="鉄筋（SD345）",
        code="M002",
        specification="D19",
        unit="t",
        unit_price=120000,
        current_stock=20,
        minimum_stock=10,
    ),
    Material.objects.create(
        category=material_categories[1],
        name="エアコン室外機",
        code="E001",
        specification="20馬力",
        unit="台",
        unit_price=800000,
        current_stock=5,
        minimum_stock=2,
    ),
    Material.objects.create(
        category=material_categories[2],
        name="ドリル",
        code="T001",
        specification="充電式18V",
        unit="台",
        unit_price=35000,
        current_stock=8,
        minimum_stock=3,
    ),
]

print("デモデータの作成が完了しました。")
