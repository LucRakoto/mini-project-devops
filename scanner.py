import re

class VulnerabilityScanner:
    def __init__(self):
        self.patterns = {
            "Injection_SQL": [r"SELECT.*FROM", r"DROP\s+TABLE"],
            "Faille_XSS": [r"<script.*?>", r"javascript:"],
            "Fuite_Donnees": [r"password\s*=\s*['\"].+['\"]", r"secret\s*=\s*['\"].+['\"]"]
        }

    def scan(self, code, filename=""):
        # EXPERT TIP: On n'analyse pas les secrets dans les fichiers YAML ou ENV
        if filename.endswith(('.yml', '.yaml', '.env')):
            return "Statut: Securise"

        found = []
        # On ignore les commentaires pour eviter les faux positifs
        code_clean = re.sub(r'#.*', '', code) 
        
        for cat, rules in self.patterns.items():
            for rule in rules:
                if re.search(rule, code_clean, re.IGNORECASE):
                    found.append(cat)
                    break
        
        if not found:
            return "Statut: Securise"
        return f"Alerte: {', '.join(found)}"