# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResConfigSettings(models.TransientModel):
  _inherit = 'res.config.settings'

  ''' CS API Credentials '''
  sm_carsharing_api_credentials_api_key = fields.Char(
    related='company_id.sm_carsharing_api_credentials_api_key',
    string=_("Carsharing API Key"),
    readonly=False)
  sm_carsharing_api_credentials_cs_url = fields.Char(
    related='company_id.sm_carsharing_api_credentials_cs_url',
    string=_("Carsharing API URL"),
    readonly=False)
  sm_carsharing_api_credentials_admin_group = fields.Char(
    related='company_id.sm_carsharing_api_credentials_admin_group',
    string=_("Carsharing Admin Group"),
    readonly=False)

  ''' WORDPRESS DB CREDENTIALS '''
  sm_wordpress_db_credentials_admin_host = fields.Char(
    related='company_id.sm_wordpress_db_credentials_admin_host',
    string=_("Wordpress DB Admin Host"),
    readonly=False)
  sm_wordpress_db_credentials_admin_username = fields.Char(
    related='company_id.sm_wordpress_db_credentials_admin_username',
    string=_("Wordpress DB Admin Username"),
    readonly=False)
  sm_wordpress_db_credentials_admin_password = fields.Char(
    related='company_id.sm_wordpress_db_credentials_admin_password',
    string=_("Wordpress DB Admin Password"),
    readonly=False)
  sm_wordpress_db_credentials_db_host = fields.Char(
    related='company_id.sm_wordpress_db_credentials_db_host',
    string=_("Wordpress DB Host"),
    readonly=False)
  sm_wordpress_db_credentials_db_username = fields.Char(
    related='company_id.sm_wordpress_db_credentials_db_username',
    string=_("Wordpress DB Username"),
    readonly=False)
  sm_wordpress_db_credentials_db_password = fields.Char(
    related='company_id.sm_wordpress_db_credentials_db_password',
    string=_("Wordpress DB Password"),
    readonly=False)
  sm_wordpress_db_credentials_db_database = fields.Char(
    related='company_id.sm_wordpress_db_credentials_db_database',
    string=_("Wordpress DB Database"),
    readonly=False)

  ''' FIREBASE AUTH CREDENTIALS '''
  sm_firebase_auth_type = fields.Char(
    related='company_id.sm_firebase_auth_type',
    string=_("Firebase Auth Type"),
    readonly=False)
  sm_firebase_auth_project_id = fields.Char(
    related='company_id.sm_firebase_auth_project_id',
    string=_("Firebase Auth Project ID"),
    readonly=False)
  sm_firebase_auth_private_key_id = fields.Char(
    related='company_id.sm_firebase_auth_private_key_id',
    string=_("Firebase Auth Private Key ID"),
    readonly=False)
  sm_firebase_auth_private_key = fields.Char(
    related='company_id.sm_firebase_auth_private_key',
    string=_("Firebase Auth Private Key"),
    readonly=False)
  sm_firebase_auth_client_email = fields.Char(
    related='company_id.sm_firebase_auth_client_email',
    string=_("Firebase Auth Client Email"),
    readonly=False)
  sm_firebase_auth_client_id = fields.Char(
    related='company_id.sm_firebase_auth_client_id',
    string=_("Firebase Auth Client ID"),
    readonly=False)
  sm_firebase_auth_auth_uri = fields.Char(
    related='company_id.sm_firebase_auth_auth_uri',
    string=_("Firebase Auth URI"),
    readonly=False)
  sm_firebase_auth_token_uri = fields.Char(
    related='company_id.sm_firebase_auth_token_uri',
    string=_("Firebase Auth Token URI"),
    readonly=False)
  sm_firebase_auth_provider_x509 = fields.Char(
    related='company_id.sm_firebase_auth_provider_x509',
    string=_("Firebase Auth Provider X509"),
    readonly=False)
  sm_firebase_auth_client_x509 = fields.Char(
    related='company_id.sm_firebase_auth_client_x509',
    string=_("Firebase Auth Client X509"),
    readonly=False)
  sm_firebase_auth_db_ref = fields.Char(
    related='company_id.sm_firebase_auth_db_ref',
    string=_("Firebase Database Reference"),
    readonly=False)
