# **live-host-triage**

Ferramenta de triagem forense para resposta a incidentes, focada na coleta de evidências voláteis de um sistema comprometido antes que ele seja desligado — evidências que se perdem permanentemente assim que a máquina é desligada.

> Nota: os campos "Próximos Passos / Roadmap" são sugestões — edite ou remova conforme os planos reais para o projeto.

---

## **Por que "live" triage?**

Em resposta a incidentes, uma das decisões mais críticas é: desligar a máquina comprometida imediatamente (contendo o ataque, mas perdendo dados voláteis) ou mantê-la ligada para coletar evidências (arriscando que o atacante continue ativo). O live-host-triage existe para reduzir esse dilema: automatiza a coleta de evidências voláteis rapidamente, para que o sistema possa ser desligado com segurança logo em seguida, sem perder rastros essenciais da investigação.

---

## **Estrutura do Projeto**

```
live-host-triage/
├── core/
│   ├── network.py      # Coleta de conexões de rede ativas e tabelas ARP
│   └── processes.py    # Coleta de processos em execução e cálculo de hash SHA-256
├── utils/
│   └── reporter.py     # Consolidação das evidências e geração do relatório (.zip)
├── triage_output/      # Diretório onde os relatórios gerados são salvos
├── triage.py           # Ponto de entrada — orquestra a coleta completa
├── __init__.py
├── requirements.txt
└── .gitignore
```

## **Funcionalidades**

* **Coleta de processos em execução (`core/processes.py`)** — lista todos os processos ativos no momento da triagem, capturando o estado do sistema antes de qualquer intervenção, e calcula o hash SHA-256 dos executáveis associados a processos suspeitos.
* **Coleta de rede (`core/network.py`)** — utiliza `netstat`/`ss` para capturar conexões de rede em andamento, essenciais para identificar comunicação com servidores de comando e controle (C2) ou exfiltração de dados em curso, além de registrar as tabelas ARP da rede local.
* **Coleta de chaves de inicialização/autostart** — verifica o Registro do Windows e serviços systemd no Linux, pontos comuns de persistência usados por malware para sobreviver a reinicializações.
* **Geração de relatório (`utils/reporter.py`)** — consolida todas as evidências coletadas em um pacote de relatório compactado (`.zip`), salvo em `triage_output/`, incluindo o nível de integridade de cada item coletado.
* **Orquestração (`triage.py`)** — ponto de entrada que executa toda a rotina de coleta em sequência.

---

## **Tecnologias Utilizadas**

* Python 3.x (100% do projeto — sem dependência de PowerShell ou scripts externos)
* `sys`, `platform`, `os` — detecção do sistema operacional e interação com o ambiente
* `datetime` (`datetime`, `timezone`) — timestamp das evidências coletadas e do relatório gerado
* Módulos internos do projeto: `core.processes` (coleta de processos), `core.network` (coleta de rede) e `utils.reporter` (geração do relatório)

---

## **Como Funciona**

O script identifica o sistema operacional do host (Windows ou Linux) e executa a rotina de coleta correspondente inteiramente em Python: consultando o Registro no Windows e lendo `/proc`, executando `ss`/`netstat` e verificando serviços systemd no Linux. Cada evidência coletada é organizada e, quando aplicável (executáveis de processos suspeitos), tem seu hash SHA-256 calculado. Ao final, tudo é consolidado em um pacote de relatório, compactado em `.zip`, pronto para análise posterior por um analista de segurança.

---

## **Como Usar**

```bash
pip install -r requirements.txt

python triage.py
```

O script é executado sem argumentos de linha de comando — a coleta de processos, conexões de rede e informações do sistema é iniciada automaticamente ao rodar o arquivo.

O relatório é gerado como um pacote compactado `.zip`, salvo em `triage_output/`, seguindo o padrão de nome `triage_package_AAAAMMDD_HHMMSS.zip` (exemplo: `triage_output/triage_package_20260924_192313.zip`).

---

## **Aviso Legal**

Esta ferramenta foi desenvolvida para fins educacionais e de prática em resposta a incidentes. O uso para coleta de evidências em sistemas de terceiros sem autorização explícita pode violar legislação local. Utilize apenas em ambientes controlados, de laboratório, ou com autorização formal.

---

## **Próximos Passos / Roadmap**

* Suporte a coleta de memória RAM completa (dump de memória) para análise forense mais profunda
* Exportação do relatório em formatos adicionais, como JSON estruturado, para integração direta com ferramentas de SIEM
* Assinatura digital do pacote de relatório, para garantir cadeia de custódia da evidência
* Suporte a coleta remota, permitindo triagem de múltiplos hosts a partir de um único ponto de controle

---

## **Autor**

**Natan Tadeu Dos Santos Coelho**
Estudante de Engenharia de Software e Cybersecurity | Futuro Engenheiro de Segurança Cibernética
