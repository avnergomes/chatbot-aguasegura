"""Domain knowledge for the Programa Água Segura chatbot."""
from __future__ import annotations

from data.document_loader import load_reference_documents

BASE_GUIDE = """
Programa Água Segura — Visão Geral
----------------------------------
O Programa Água Segura é uma iniciativa integrada que apoia municípios, técnicos, produtores rurais e demais parceiros na garantia de acesso contínuo à água potável e à gestão sustentável dos recursos hídricos. Ele combina ações de infraestrutura hídrica, educação ambiental, assistência técnica e monitoramento participativo para promover saúde pública, produção sustentável e resiliência climática.

Públicos Prioritários e Benefícios
----------------------------------
* **Gestores municipais** recebem apoio para diagnóstico hídrico, elaboração de planos de segurança da água (PSA) e captação de recursos.
* **Técnicos de campo** contam com protocolos de monitoramento da qualidade da água, orientações para implantação de tecnologias sociais, e ferramentas de acompanhamento de indicadores.
* **Produtores rurais e comunidades** têm acesso a capacitações em manejo do solo e da água, práticas agroecológicas, proteção de nascentes, saneamento rural e reúso seguro.
* **Parceiros institucionais** encontram diretrizes para cofinanciamento, integração de políticas públicas e transparência dos resultados.

Componentes do Programa
-----------------------
1. **Diagnóstico e Planejamento** – Levantamento participativo de fontes hídricas, avaliação de riscos sanitários, priorização de intervenções e construção do Plano de Ação Municipal.
2. **Infraestrutura e Tecnologias** – Implantação de sistemas de captação (chuva, poços, adutoras), reservação, tratamento simplificado, distribuição e soluções de saneamento ecológico.
3. **Educação e Mobilização** – Campanhas de educação ambiental, fortalecimento dos comitês comunitários, formação de agentes multiplicadores e comunicação transparente.
4. **Assistência Técnica Contínua** – Visitas técnicas, roteiros de boas práticas, apoio à operação e manutenção dos sistemas e suporte à gestão comunitária.
5. **Monitoramento e Avaliação** – Indicadores de qualidade da água, cobertura do atendimento, governança e sustentabilidade financeira, com painéis periódicos de resultados.

Diretrizes Técnicas Essenciais
-----------------------------
* O Plano de Segurança da Água deve considerar perigos físicos, químicos e biológicos, medidas preventivas, controle operacional e planos de contingência.
* Sistemas de tratamento devem respeitar normas da Portaria GM/MS nº 888/2021, garantindo turbidez < 5 NTU, cloro residual entre 0,2 e 2 mg/L e ausência de E. coli em 100 mL.
* Nascentes devem ser protegidas com cercamento, controle de erosão, recarga de aquíferos e reflorestamento de matas ciliares.
* Para comunidades rurais, recomenda-se priorizar tecnologias de baixo custo e fácil manutenção, como filtros lentos, cloradores simples, cisternas, wetlands construídas e fossas sépticas biodigestoras.
* O monitoramento participativo envolve capacitar moradores para coleta de amostras, leitura de testes rápidos, registro em planilhas digitais e reporte aos técnicos municipais.

Indicadores de Sucesso
----------------------
* Percentual de domicílios com acesso contínuo à água potável.
* Redução de surtos de doenças de veiculação hídrica.
* Número de nascentes protegidas e hectares recuperados.
* Sustentabilidade financeira medida pelo equilíbrio entre custos operacionais e tarifas comunitárias/recursos públicos.
* Participação social em comitês e reuniões de avaliação.

Perguntas Frequentes
--------------------
* **Como iniciar um PSA?** – Reúna equipe multidisciplinar, mapeie o sistema de abastecimento, identifique perigos e defina medidas de controle com cronograma e responsáveis.
* **Quais recursos financeiros podem ser acessados?** – Programas federais (FUNASA, MDR), fundos estaduais de recursos hídricos, cooperação internacional e parcerias com ONGs.
* **Como envolver produtores?** – Ofereça assistência técnica em conservação de solo, incentivos para práticas agroecológicas, apoio para cercamento de APPs e certifique benefícios econômicos.
* **Qual é a rotina mínima de monitoramento?** – Verificação diária do cloro, medição semanal de turbidez e pH, análises microbiológicas mensais e relatórios trimestrais para gestão municipal.
""".strip()


def _format_document_section(title: str, content: str) -> str:
    """Format a reference document into a prompt friendly section."""
    separator = "-" * len(title)
    return f"{title}\n{separator}\n{content.strip()}"


def build_program_knowledge() -> str:
    """Compose the full knowledge base from the core guide and repository documents."""
    sections = [BASE_GUIDE]

    for identifier, content in load_reference_documents().items():
        display_name = identifier.replace("_", " ").title()
        sections.append(_format_document_section(f"Documento de Referência: {display_name}", content))

    return "\n\n".join(section for section in sections if section)


PROGRAM_KNOWLEDGE = build_program_knowledge()
