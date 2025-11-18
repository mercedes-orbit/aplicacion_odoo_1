{
    "name": "Nuevo Módulo CURSO ODOO",
    "summary": "Aprender a crear un nuevo módulo",
    "version": "17.0.0.14", #cambiar para subir automaticamente
    "author": "Mercedes Galán",
    "license": "AGPL-3",
    "website": "https://orbit.com",
    "category": "Accounting & Finance",
    "depends": ["contacts","sale_management"], #añadir '?debug=1' detras de 'web' en la URL de workspace odoo y ver nombre modulo en APPS y ponerlo aqui
    #"external_dependencies": {"python": ["unidecode"]},
    "data": ["security/ir.model.access.csv",
             "views/state_property_tag_views.xml", 
             "views/organismo_views.xml",
             "views/state_property_type_views.xml",
             "views/state_property_offer_views.xml", 
             "views/state_property_views.xml",
    ],
    "installable": True
    #"pre_init_hook": "pre_init_hook",
}
