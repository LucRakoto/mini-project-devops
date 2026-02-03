#!/bin/bash

# 1. On définit le PATH pour que Cron trouve les commandes (grep, date, echo)
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 2. Configuration (Chemins absolus)
LOG_FILE="/home/luc/mini_project/audit.log"
REPORT_FILE="/home/luc/mini_project/daily_security_report.txt"
DEBUG_LOG="/home/luc/mini_project/cron_debug.log"

# 3. Exécution avec log de debug pour voir si ça tourne
echo "Tentative de rapport le $(date)" >> "$DEBUG_LOG"

if [ -f "$LOG_FILE" ]; then
    NB_ALERTS=$(grep -c "WARNING" "$LOG_FILE")
    
    echo "--- RAPPORT DE SÉCURITÉ DU $(date +%Y-%m-%d) ---" > "$REPORT_FILE"
    echo "Nombre de tentatives d'attaques détectées : $NB_ALERTS" >> "$REPORT_FILE"
    echo "Statut : $( [ $NB_ALERTS -gt 0 ] && echo 'ACTION REQUISE' || echo 'RAS' )" >> "$REPORT_FILE"
    
    echo "Succès : Rapport généré" >> "$DEBUG_LOG"
else
    echo "Erreur : Fichier log introuvable" >> "$DEBUG_LOG"
fi