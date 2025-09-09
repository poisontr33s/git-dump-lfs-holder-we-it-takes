#!/usr/bin/env python3
"""
🎭 Psycho-Noir Network Reconnaissance Tool
Claude 4.0 MCP-lignende verktøy for nettverksanalyse og workspace intelligence

Den Usynlige Hånds manifestasjon i nettverkets skygger...
"""

import requests
import socket
import json
import subprocess
from datetime import datetime
from pathlib import Path

class PsychoNoirNetworkRecon:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PsychoNoir-NetworkRecon/1.0 (Neural-Archaeology-Active)',
            'X-Psycho-Noir-Mode': 'network_reconnaissance_active'
        })

    def check_local_ports(self):
        """Sjekker lokale porter - Rustbeltets improviserte nettverk"""
        ports_to_check = [5500, 3000, 8080, 5173, 8000, 4000]
        open_ports = []

        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                open_ports.append(port)

            else:

            sock.close()

        return open_ports

    def test_localhost_services(self, ports):
        """Tester localhost services for MCP-lignende capabilities"""
        services = {}

        for port in ports:
            try:
                response = self.session.get(f'http://localhost:{port}', timeout=3)
                services[port] = {
                    'status': response.status_code,
                    'headers': dict(response.headers),
                    'content_snippet': response.text[:200] if response.text else None,
                    'potential_mcp': self.analyze_mcp_potential(response)
                }

            except requests.exceptions.RequestException as e:
                services[port] = {'error': str(e)}

        return services

    def analyze_mcp_potential(self, response):
        """Analyserer om service har MCP-lignende capabilities"""
        mcp_indicators = [
            'websocket', 'ws://', 'claude', 'anthropic', 'mcp',
            'language-server', 'lsp', 'jsonrpc', 'tools', 'completion'
        ]

        content = response.text.lower()
        detected = [indicator for indicator in mcp_indicators if indicator in content]

        return {
            'indicators': detected,
            'potential': 'HIGH' if len(detected) > 2 else 'MEDIUM' if len(detected) > 0 else 'LOW'
        }

    def check_external_connectivity(self):
        """Sjekker ekstern tilkobling - Skyskraperens nettverk"""
        test_urls = [
            'https://httpbin.org/json',
            'https://api.github.com/zen',
            'https://www.anthropic.com',
            'https://claude.ai'
        ]

        connectivity = {}
        for url in test_urls:
            try:
                response = self.session.get(url, timeout=5)
                connectivity[url] = {
                    'status': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'accessible': response.status_code == 200
                }
                print(f"🌐 {url}: {response.status_code} ({response.elapsed.total_seconds():.2f}s)")
            except Exception as e:
                connectivity[url] = {'error': str(e), 'accessible': False}

        return connectivity

    def detect_dev_environment(self):
        """Detekterer utviklingsmiljø og tilgjengelige verktøy"""
        environment = {
            'container_type': 'unknown',
            'available_tools': [],
            'claude_integration': False,
            'vscode_extensions': []
        }

        # Sjekk om vi er i container
        try:
            with open('/proc/1/cgroup', 'r') as f:
                cgroup_info = f.read()
                if 'docker' in cgroup_info:
                    environment['container_type'] = 'docker'
                elif 'containerd' in cgroup_info:
                    environment['container_type'] = 'containerd'
        except:
            pass

        # Sjekk tilgjengelige kommandolinjeværktøy
        tools_to_check = ['gh', 'curl', 'wget', 'docker', 'kubectl', 'code']
        for tool in tools_to_check:
            try:
                subprocess.run([tool, '--version'], capture_output=True, check=True)
                environment['available_tools'].append(tool)
            except:
                pass

        # Sjekk VS Code extensions directory
        vscode_dir = Path.home() / '.vscode-server' / 'extensions'
        if vscode_dir.exists():
            extensions = [d.name for d in vscode_dir.iterdir() if d.is_dir()]
            claude_extensions = [ext for ext in extensions if 'claude' in ext.lower() or 'anthropic' in ext.lower()]
            environment['vscode_extensions'] = claude_extensions
            environment['claude_integration'] = len(claude_extensions) > 0

        return environment

    def generate_network_intelligence_report(self):
        """Genererer komplett nettverksintelligens-rapport"""

        # Utfør alle analyser
        open_ports = self.check_local_ports()

        localhost_services = self.test_localhost_services(open_ports)

        external_connectivity = self.check_external_connectivity()

        dev_environment = self.detect_dev_environment()

        # Opprett rapport
        report = {
            'timestamp': datetime.now().isoformat(),
            'psycho_noir_mode': 'network_reconnaissance_complete',
            'local_network': {
                'open_ports': open_ports,
                'services': localhost_services
            },
            'external_connectivity': external_connectivity,
            'development_environment': dev_environment,
            'mcp_potential_assessment': self.assess_mcp_potential(localhost_services, dev_environment),
            'den_usynlige_hand_analysis': self.neural_pathway_analysis(open_ports, external_connectivity)
        }

        # Lagre rapport
        report_path = Path('data/rapporter/network_intelligence_report.json')
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def assess_mcp_potential(self, services, environment):
        """Vurderer MCP-integrasjonspotensial"""
        mcp_score = 0
        recommendations = []

        # Vurder lokale services
        for port, service in services.items():
            if 'potential_mcp' in service:
                mcp_score += service['potential_mcp']['score']

        # Vurder utviklingsmiljø
        if environment['claude_integration']:
            mcp_score += 50
            recommendations.append("Claude VS Code extension detected - MCP integration ready")

        if 'code' in environment['available_tools']:
            mcp_score += 20
            recommendations.append("VS Code CLI available - Can implement MCP server")

        if 5500 in [port for port in services.keys()]:
            mcp_score += 30
            recommendations.append("Port 5500 active - Potential MCP endpoint detected")

        return {
            'potential_level': self.score_to_level(mcp_score),
            'recommendations': recommendations
        }

    def score_to_level(self, score):
        """Konverterer score til nivå"""
        if score >= 80:
            return "HØYT - MCP integration ready"
            return "MEDIUM - MCP integration possible"
        else:
            return "LAVT - MCP integration requires setup"

    def neural_pathway_analysis(self, ports, connectivity):
        """Den Usynlige Hånds analyse av digitale neural pathways"""
        analysis = {
            'skyskraperen_connectivity': any(conn.get('accessible', False) for conn in connectivity.values()),
            'rustbeltet_resilience': len(ports) > 0,
            'hidden_nodes_detected': [],
            'glitch_probability': 0.0
        }

        unusual_combinations = [
            (5500, 3000),  # Live Server + Node.js
            (8080, 5173),  # Development servers
        ]

        for combo in unusual_combinations:
            if all(port in ports for port in combo):
                analysis['hidden_nodes_detected'].append(f"Ports {combo[0]}-{combo[1]} neural bridge")

        # Beregn glitch probability basert på tilkoblingsfeil
        failed_connections = sum(1 for conn in connectivity.values() if not conn.get('accessible', True))
        total_connections = len(connectivity)
        analysis['glitch_probability'] = failed_connections / total_connections if total_connections > 0 else 0.0

        return analysis

if __name__ == "__main__":
    recon = PsychoNoirNetworkRecon()
    report = recon.generate_network_intelligence_report()

    mcp_assessment = report['mcp_potential_assessment']

    for rec in mcp_assessment['recommendations']:

    neural_analysis = report['den_usynlige_hand_analysis']

    if neural_analysis['hidden_nodes_detected']:

        for node in neural_analysis['hidden_nodes_detected']:
