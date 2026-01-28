import re

class VulnerabilityScanner:
    def __init__(self):
        # On définit les signatures de menaces
        self.patterns = {
            "Injection SQL": [r"'.*or.*=.*", r"--", r"drop\s+table", r"union\s+select"],
            "XSS (Script)": [r"<script>", r"javascript:", r"onerror="],
            "Fuite de données": [r"password\s*=", r"api_key\s*=", r"secret\s*="]
        }

    def scan(self, code):
        found_issues = []
        code_lower = code.lower()

        for category, rules in self.patterns.items():
            for rule in rules:
                if re.search(rule, code_lower):
                    found_issues.append(category)
                    break
        
        if not found_issues:
            return "✅ SÉCURISÉ"
        return f"❌ VULNÉRABLE : {', '.join(found_issues)}"