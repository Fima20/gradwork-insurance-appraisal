SERVER_HOST = '0.0.0.0'#localhost
SERVER_PORT = 5005
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
PROJECT_FOLDER = ''
UPLOAD_FOLDER = 'static/'
TEMPLATE_FOLDER = 'templates/'


# <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}" />
# <link rel="stylesheet" type="text/css" href="../static/css/style.css" />
# <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css" />
# <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">


# {% if True %}
# <a href="{{ url_for('auth.signup') }}" class="navbar-item may">
#     Регистрация
# </a>
# {% endif %}

# def contracts_add_post(id_contract=None):
#
#     def url_error():
#         if id_contract:
#             return redirect(url_for('main.contract_add_get',
#                                     id_contract=id_contract,
#                                     contract_status="error"))
#         else:
#             return redirect(url_for('main.contracts_add', contract_status="error"))
#
#     company_name = request.form.get('company_name')
#     id_company = api_db.getid_company(name=company_name)
#     if id_company:
#         company_create = api_db.update_company(name=company_name, idcompany=id_company)
#     else:
#         company_create = api_db.add_company(name=company_name)
#         id_company = api_db.getid_company(name=company_name)
#     if not company_create: return url_error()
#
#     passport_series = int(request.form.get('client_passport_series'))
#     passport_id = int(request.form.get('client_passport_id'))
#     id_client = api_db.getid_client(passport_series=passport_series, passport_id=passport_id)
#     if id_client:
#         client_create = api_db.update_client(name=request.form.get('client_name'),
#                                              surname=request.form.get('client_surname'),
#                                              sec_name=request.form.get('client_sec_name'),
#                                              passport_series=passport_series,
#                                              passport_id=passport_id,
#                                              idclient=id_client)
#     else:
#         client_create = api_db.add_client(name=request.form.get('client_name'),
#                                           surname=request.form.get('client_surname'),
#                                           sec_name=request.form.get('client_sec_name'),
#                                           passport_series=passport_series,
#                                           passport_id=passport_id)
#         id_client = api_db.getid_client(passport_series=passport_series, passport_id=passport_id)
#     if not client_create: return url_error()
#
#     title = request.form.get('type_insurance_name')
#     short_title = request.form.get('type_insurance_small_name')
#     id_insurance_type = api_db.getid_insurance_type(title=title, short_title=short_title)
#     if id_insurance_type:
#         insurance_type_create = api_db.update_insurance_type(title=title,
#                                                              short_title=request.form.get('type_insurance_small_name'),
#                                                              capital=request.form.get('type_insurance_capital'),
#                                                              idinsurance_type=id_insurance_type)
#     else:
#         insurance_type_create = api_db.add_insurance_type(title=title,
#                                                           short_title=request.form.get('type_insurance_small_name'),
#                                                           capital=request.form.get('type_insurance_capital'))
#         id_insurance_type = api_db.getid_insurance_type(title=title)
#     if not insurance_type_create: return url_error()
#
#     insurance_amount = request.form.get('insurance_amount')
#     insurance_payment = request.form.get('insurance_payment')
#     date_start = request.form.get('date_start')
#     date_stop = request.form.get('date_stop')
#     id_unit = api_db.getid_default_unit()
#     id_agent = session['idagent']
#
#     id_contract = api_db.getid_contract(id_client=id_client)
#     if id_contract:
#         contract_create = api_db.update_contract(id_client=id_client,
#                                                  id_company=id_company,
#                                                  id_unit=id_unit,
#                                                  id_insurance_type=id_insurance_type,
#                                                  id_agent=id_agent,
#                                                  insurance_amount=insurance_amount,
#                                                  insurance_payment=insurance_payment,
#                                                  date_start=date_start,
#                                                  date_stop=date_stop,
#                                                  idcontract=id_contract)
#         contract_status = "update"
#     else:
#         contract_create = api_db.add_contract(id_client=id_client,
#                                               id_company=id_company,
#                                               id_unit=id_unit,
#                                               id_insurance_type=id_insurance_type,
#                                               id_agent=id_agent,
#                                               insurance_amount=insurance_amount,
#                                               insurance_payment=insurance_payment,
#                                               date_start=date_start,
#                                               date_stop=date_stop)
#         id_contract = api_db.getid_contract(id_client=id_client)
#         contract_status = "create"
#     if not contract_create: return url_error()
#
#     return redirect(url_for('main.contract_add_get',
#                             id_contract=id_contract,
#                             contract_status=contract_status))