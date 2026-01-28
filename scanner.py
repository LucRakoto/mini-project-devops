import re

class VulnerabilityScanner:
    def __init__(self):
        # Signatures de menaces précises pour éviter les faux positifs
        self.patterns = {
            "Injection SQL": [r"'.*or.*=.*", r"--", r"drop\s+table", r"union\s+select"],
            "Faille XSS": [r"<script>", r"javascript:", r"onerror="],
            "Fuite de donnees": [r"password\s*=\s*['\"].+['\"]", r"api_key\s*=\s*['\"].+['\"]"]
        }

    def scan(self, code):
        found_issues = []
        # On travaille en minuscule pour ne rater aucune attaque
        code_lower = code.lower()

        for category, rules in self.patterns.items():
            for rule in rules:
                if re.search(rule, code_lower):
                    found_issues.append(category)
                    break
        
        # Messages simplifiés sans accents pour GitHub Actions
        if not found_issues:
            return "Statut: Securise"
        
        return f"Alerte: {', '.join(found_issues)}"