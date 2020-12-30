output "client_key" {
  value = module.dirtbag_instantiation.cient_key
}

output "client_secret" {
  value = module.dirtbag_instantiation.client_secret
}

output "client_config" {
  value = module.dirtbag_instantiation.web_ui_config_json
}

resource "local_file" "web-config" {
  filename = "config.json"
  content = module.dirtbag_instantiation.web_ui_config_json
}
