FILES_TYPE_CHOICES = ( 
    ("customer_images", "customer_images"), 
    )

LOAN_RECURRENCE_CHOICES = (
    ("daily", "daily"),
    ("weekly", "weekly"),
    ("biweekly", "biweekly"),
    ("monthly", "monthly"),
)

WALLET_MOVEMENT_TYPE_CHOICES = (
    ("entry", "entry"),
    ("exit", "exit"),
)

CUSTOMER_TYPE_CHOICES = (
    ('new', 'new'),
    ('old', 'old'),
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