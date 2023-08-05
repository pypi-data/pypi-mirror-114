from setuptools import setup

name = "types-braintree"
description = "Typing stubs for braintree"
long_description = '''
## Typing stubs for braintree

This is a PEP 561 type stub package for the `braintree` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `braintree`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/braintree. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `955a3e5d9d5a35382ad6d0c24985dcd27df8f7f6`.
'''.lstrip()

setup(name=name,
      version="4.11.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['braintree-stubs'],
      package_data={'braintree-stubs': ['version.pyi', 'us_bank_account.pyi', 'subscription_details.pyi', 'samsung_pay_card.pyi', 'ids_search.pyi', 'merchant_gateway.pyi', 'credit_card_verification_search.pyi', 'account_updater_daily_report.pyi', 'customer_gateway.pyi', 'bin_data.pyi', 'transaction_line_item_gateway.pyi', 'paypal_account_gateway.pyi', 'apple_pay_card.pyi', 'validation_error_collection.pyi', 'discount.pyi', 'oauth_credentials.pyi', 'oauth_access_revocation.pyi', 'three_d_secure_info.pyi', 'webhook_testing_gateway.pyi', 'payment_method_nonce_gateway.pyi', 'customer.pyi', 'merchant.pyi', 'document_upload.pyi', 'resource_collection.pyi', 'customer_search.pyi', 'transaction_details.pyi', 'address_gateway.pyi', 'oauth_gateway.pyi', 'credit_card.pyi', 'disbursement_detail.pyi', 'webhook_testing.pyi', 'us_bank_account_gateway.pyi', 'client_token.pyi', 'merchant_account_gateway.pyi', 'attribute_getter.pyi', 'status_event.pyi', 'credit_card_verification_gateway.pyi', 'payment_method.pyi', 'connected_merchant_status_transitioned.pyi', 'modification.pyi', 'authorization_adjustment.pyi', 'facilitated_details.pyi', 'credit_card_verification.pyi', 'paginated_collection.pyi', 'visa_checkout_card.pyi', 'configuration.pyi', 'discount_gateway.pyi', 'venmo_account.pyi', 'revoked_payment_method_metadata.pyi', 'subscription_search.pyi', 'us_bank_account_verification_gateway.pyi', 'granted_payment_instrument_update.pyi', 'dispute_search.pyi', 'europe_bank_account.pyi', 'local_payment_completed.pyi', 'resource.pyi', 'connected_merchant_paypal_status_changed.pyi', 'dispute.pyi', 'amex_express_checkout_card.pyi', 'paginated_result.pyi', 'credentials_parser.pyi', 'payment_method_nonce.pyi', 'plan.pyi', 'add_on.pyi', 'android_pay_card.pyi', 'transaction.pyi', 'local_payment_reversed.pyi', 'us_bank_account_verification_search.pyi', 'payment_instrument_type.pyi', 'transaction_gateway.pyi', 'processor_response_types.pyi', 'subscription.pyi', 'errors.pyi', 'paypal_account.pyi', 'error_codes.pyi', 'credit_card_gateway.pyi', 'webhook_notification_gateway.pyi', 'settlement_batch_summary_gateway.pyi', 'descriptor.pyi', 'validation_error.pyi', 'ach_mandate.pyi', 'braintree_gateway.pyi', 'settlement_batch_summary.pyi', 'payment_method_parser.pyi', 'unknown_payment_method.pyi', 'local_payment.pyi', 'payment_method_gateway.pyi', 'error_result.pyi', 'client_token_gateway.pyi', 'iban_bank_account.pyi', 'address.pyi', 'paypal_here.pyi', 'us_bank_account_verification.pyi', 'plan_gateway.pyi', 'signature_service.pyi', 'transaction_line_item.pyi', '__init__.pyi', 'add_on_gateway.pyi', 'environment.pyi', 'document_upload_gateway.pyi', 'successful_result.pyi', 'transaction_search.pyi', 'partner_merchant.pyi', 'disbursement.pyi', 'apple_pay_options.pyi', 'dispute_gateway.pyi', 'subscription_status_event.pyi', 'facilitator_details.pyi', 'testing_gateway.pyi', 'apple_pay_gateway.pyi', 'search.pyi', 'subscription_gateway.pyi', 'webhook_notification.pyi', 'masterpass_card.pyi', 'risk_data.pyi', 'transaction_amounts.pyi', 'exceptions/too_many_requests_error.pyi', 'exceptions/invalid_signature_error.pyi', 'exceptions/configuration_error.pyi', 'exceptions/upgrade_required_error.pyi', 'exceptions/unexpected_error.pyi', 'exceptions/gateway_timeout_error.pyi', 'exceptions/authentication_error.pyi', 'exceptions/braintree_error.pyi', 'exceptions/authorization_error.pyi', 'exceptions/service_unavailable_error.pyi', 'exceptions/invalid_challenge_error.pyi', 'exceptions/__init__.pyi', 'exceptions/not_found_error.pyi', 'exceptions/request_timeout_error.pyi', 'exceptions/server_error.pyi', 'exceptions/http/connection_error.pyi', 'exceptions/http/timeout_error.pyi', 'exceptions/http/invalid_response_error.pyi', 'exceptions/http/__init__.pyi', 'dispute_details/status_history.pyi', 'dispute_details/evidence.pyi', 'dispute_details/paypal_message.pyi', 'dispute_details/__init__.pyi', 'merchant_account/business_details.pyi', 'merchant_account/individual_details.pyi', 'merchant_account/address_details.pyi', 'merchant_account/funding_details.pyi', 'merchant_account/merchant_account.pyi', 'merchant_account/__init__.pyi', 'util/parser.pyi', 'util/constants.pyi', 'util/crypto.pyi', 'util/generator.pyi', 'util/http.pyi', 'util/__init__.pyi', 'util/xml_util.pyi', 'util/graphql_client.pyi', 'util/datetime_parser.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
