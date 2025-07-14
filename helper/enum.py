import enum
class LevelCor(enum.Enum):
    small_retail = 1
    departement_store = 2
    warehouse = 3
    convenience = 4
    speciality = 5
    mobile_retail = 6
    internet_retail = 7
    
class LevelRole(enum.Enum):
    SuperAdmin = "superadmin"
    adminTeam = "adminTeam"
    supportTeam = "supportTeam"
    Admin = "admin"
    Staff = "staff"
    Manager = "manager"
    Kasir = "kasir"
    Support = "support"
    Sales = "sales"
    Owner = "owner"
    Accounting = "accounting"
    Supervisor = "supervisor"
    
class DirectoryFiles(enum.Enum):
    Stores = "resources/stores/"
    Items = "resources/items/"
    Outlet = "resources/outlet/"
    Products = "resources/product/"