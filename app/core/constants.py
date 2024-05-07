FILES_TYPE_CHOICES = ( 
    ("customer_images", "customer_images"),
    )

LOAN_RECURRENCE_CHOICES = (
    ("daily", "Diario"),
    ("weekly", "Semanal"),
    ("biweekly", "Quincenal"),
    ("monthly", "Mensual"),
)

WALLET_MOVEMENT_TYPE_CHOICES = (
    ("entry", "Ingreso"),
    ("exit", "Gasto"),
    ("loan_out", "Salida por prestamo"),
    ("loan_in", "Entrada por prestamo"),
    ("admin_charge", "Recarga de administracion"),
)

CUSTOMER_TYPE_CHOICES = (
    ('new', 'Nuevo'),
    ('old', 'Antiguo'),
)

REQUIRED_FIELDS_CUSTOMER_LOAN = {
    'new': [
        'document_number',
        'name',
        'home_address',
        'business_name',
        'business_address',
        'cell_phone_number',
        'occupation',
        'alias_or_reference',
    ],
    'old': [
        'customer',
    ]
}