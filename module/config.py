class Regular:
    ip_address: str = "^\\b((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\b$"
    domain_name: str = "^\\b(((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)|((?!-)[A-Za-z\\d-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6})\\b$"
    agent_address: str = "^\\b(((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)|((?!-)[A-Za-z\\d-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}):(6553[0-5]|655[0-2]\\d|65[0-4]\\d{2}|6[0-4]\\d{3}|[1-5]\\d{4}|[1-9]\\d{1,3}|\\d)\\b$"


regular_expression: Regular = Regular()
