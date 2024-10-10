import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

django.setup()

from accounts.models import Subject
subjects = {
    "Português",
    "Matemática",
    "Ciências",
    "História",
    "Geografia",
    "Artes",
    "Educação Física",
    "Língua Estrangeira (Inglês, Espanhol)",
    "Ensino Religioso",
    "Tecnologia da Informação",
    "Química",
    "Física",
    "Biologia",
    "Filosofia",
    "Sociologia",
    "Empreendedorismo",
    "Educação Financeira",
    "Programação",
    "Redes de Computadores",
    "Design Gráfico",
    "Marketing",
    "Administração",
    "Eletrônica",
    "Mecânica",
    "Enfermagem",
    "Segurança do Trabalho",
    "Agricultura e Pecuária",
    "Logística",
    "Recursos Humanos",
    "Hotelaria e Turismo",
    "Saúde Bucal",
    "Moda e Estilismo",
    "Estatística",
    "Engenharia (Civil, Elétrica, Mecânica, de Software)",
    "Ciência da Computação",
    "Arquitetura e Urbanismo",
    "Agronomia",
    "Psicologia",
    "Antropologia",
    "Comunicação Social",
    "Relações Internacionais",
    "Direito",
    "Serviço Social",
    "Medicina",
    "Farmácia",
    "Nutrição",
    "Biomedicina",
    "Odontologia",
    "Veterinária",
    "Economia",
    "Contabilidade",
    "Gestão de Recursos Humanos",
    "Publicidade e Propaganda",
    "Música",
    "Dança",
    "Teatro",
    "Artes Visuais",
    "Cinema",
    "Literatura",
    "MBA em Administração",
    "Mestrado em Educação",
    "Mestrado em Psicologia",
    "Doutorado em Ciências",
    "Especialização em Marketing Digital",
    "Especialização em Saúde Pública",
    "Especialização em Engenharia de Software",
    "Inteligência Artificial",
    "Análise de Dados",
    "Sustentabilidade",
    "Ética Profissional",
    "Diversidade e Inclusão",
}


def populate_subjects():
    for subject in subjects:
        if not Subject.objects.filter(name=subject).exists():
            Subject.objects.create(name=subject)
            
if __name__ == "__main__":
    populate_subjects()