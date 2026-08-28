call openapi-generator-cli generate ^
  -i "%~dp0gbs3-openapi.json" ^
  -g python ^
  -o "%~dp0gbs3api" ^
  -c "%~dp0config-gbs3.yaml"