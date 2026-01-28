import re

class VulnerabilityScanner:
    def __init__(self):
        self.patterns = {
            "SQL_Injection": [r"'.*or.*=.*", r"drop\s+table"],
            "XSS_Faille": [r"<script>", r"javascript:"],
            "Fuite_Donnees": [r"password\s*=\s*['\"].+['\"]"]
        }

    def scan(self, code):
        found = []
        code_lower = code.lower()
        for cat, rules in self.patterns.items():
            for rule in rules:
                if re.search(rule, code_lower):
                    found.append(cat)
                    break
        
        if not found:
            return "Statut: Securise"
        return f"Alerte: {', '.join(found)}"