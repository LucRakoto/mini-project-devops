#!/bin/bash

# Configuration
LOG_FILE="/home/luc/mini_project/audit.log"

echo "===================================================="
echo "   SYSTÈME DE SURVEILLANCE BLUE TEAM ACTIVÉ"
echo "===================================================="
echo "En attente de détections sur $LOG_FILE..."

# Surveillance en temps réel
tail -f "$LOG_FILE" | while read -r LINE
do
    if echo "$LINE" | grep -q "WARNING"; then
        echo -e "\033[0;31m[ALERTE SÉCURITÉ]\033[0m Tentative suspecte détectée !"
        echo "Détails : $LINE"
        echo "----------------------------------------------------"
    fi
done