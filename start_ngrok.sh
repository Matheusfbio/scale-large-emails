
#!/bin/bash

# Script para iniciar o ngrok como alternativa ao port forwarding do Cursor
# Este script resolve o problema "Unable to forward localhost:1222. spawn /opt/Cursor/usr/share/cursor/bin/code-tunnel ENOENT"

echo "🚀 Iniciando ngrok para port forwarding..."
echo "📱 URL pública será exibida abaixo:"
echo ""

# Iniciar ngrok na porta 8000 (Django)
ngrok http 8000

echo ""
echo "✅ ngrok iniciado com sucesso!"
echo "🌐 Acesse a URL pública acima para acessar seu Django de qualquer lugar"
echo "📊 Painel de controle: http://localhost:4040"


