import requests
import json


def OdooSaleOrderTool(ENDPOINT_ODOO='http://yokosuka.odoo.com',
                      odoo_db='odoo-ps-psus-yokosuka-production-12340670',
                      username='ramon@industrialpanasonic.com',
                      password='Imaginedragons'):
    # Paso 1: Autenticación para obtener session_id
    auth_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": odoo_db,
            "login": username,
            "password": password
        },
        "id": 1
    }

    try:
        auth_response = requests.post(f'{ENDPOINT_ODOO}/web/session/authenticate', json=auth_payload)

        auth_response.raise_for_status()

        auth_result = auth_response.json()

        if 'error' in auth_result:
            print("Authentication failed:", auth_result['error'])
            return json.dumps({"error": "Authentication failed. Please check your credentials."})

        cookies = auth_response.cookies

        headers = {"Content-Type": "application/json"}

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "account.move",
                "method": "search_read",
                "args": [
                    [
                        "|",
                        ["partner_id", "=", 95465],
                        ["partner_id.parent_id", "=", 95465],
                        ["move_type", "=", "out_invoice"],
                        ["state", "!=", "cancel"],
                        ["x_studio_portal_check", "=", True]
                    ]
                ],
                "kwargs": {
                    "fields": ["id", "name", "invoice_date", "x_studio_estado_de_pago", "x_studio_estado_de_la_factura", "amount_total", "currency_id", "x_studio_fecha_de_pago"],
                    "limit": 100
                }
            }
        }

        # Realizar la consulta usando las cookies para autenticar la sesión
        response = requests.post(f'{ENDPOINT_ODOO}/web/dataset/call_kw', json=payload, headers=headers, cookies=cookies)
        response.raise_for_status()
        result = response.json()
        print(result)
        if not result.get("result"):
            return json.dumps({"message": "No information found."})

        return json.dumps({"status": "success", "data": result["result"]})

    except requests.RequestException as e:
        return json.dumps({"error": f"Error contacting Odoo: {str(e)}"})


