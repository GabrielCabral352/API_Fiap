import django
from django.db import models
import datetime
import pandas as pd


class Turma(models.Model):
    cod_turma = models.CharField(max_length=50, default='')
    nome = models.CharField(max_length=50)
    periodo = models.CharField(max_length=15, default='1',
                    choices=(('1','Manhã'),
                             ('2','Tarde'),
                             ('3','Noite')))
    dataInicio = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField(max_length=50)
    ra = models.CharField(max_length=8)
    cpf = models.CharField(max_length=15, default='')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    identificador = models.CharField(max_length=30)
    senha = models.CharField(max_length=50)
    nivelAcesso = models.CharField(max_length=15, default='1',
                    choices=(('1','Aluno'),
                             ('2','Professor'),
                             ('3','Analista'),
                             ('4','Coordenador')))

    def __str__(self):
        return self.nome

class Materia(models.Model):
    nome = models.CharField(max_length=50)
    professor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Assinatura(models.Model):
    docente = models.ImageField(null=True, upload_to='docente/%y/%m/%d/')
    coordenador = models.ImageField(null=True, upload_to='coordenador/%y/%m/%d/')
    social = models.ImageField(null=True, upload_to='social/%y/%m/%d/')
    aluno = models.ImageField(null=True, upload_to='aluno/%y/%m/%d/')
    responsavel = models.ImageField(null=True, upload_to='responsavel/%y/%m/%d/')

    def __str__(self):
        return str(self.id)

class Fiap(models.Model):
    progresso = models.CharField(max_length=20, default='1',
                    choices=(('1','Iniciada'),
                             ('2','Em Análise'),
                             ('3','Finalizada')))

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    dataInicio = models.DateTimeField(default=datetime.datetime.now())
    dataFinal = models.DateTimeField(null=True, default=datetime.datetime.now())
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    assinatura = models.ForeignKey(Assinatura,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Frequencia(models.Model):
    aulasprevistas = models.IntegerField()
    ausencias = models.IntegerField()
    fiap = models.ForeignKey(Fiap, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Aproveitamento(models.Model):
    materia = models.ForeignKey(Materia, blank=True, on_delete=models.CASCADE)
    notamedia = models.IntegerField()
    notaaluno = models.IntegerField()
    notarec = models.IntegerField(null=True, blank=True)
    fiap = models.ForeignKey(Fiap, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Aprendizagem(models.Model):
    atencao = models.BooleanField(default=False, null=True, blank=True)
    compreensao = models.BooleanField(default=False, null=True, blank=True)
    comprometimento = models.BooleanField(default=False, null=True, blank=True)
    relacionamento = models.BooleanField(default=False, null=True, blank=True)
    Outros = models.CharField(max_length=100, null=True, blank=True)
    fiap = models.ForeignKey(Fiap, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Ocorrencia(models.Model):
    advverbal = models.BooleanField(default=False, null=True, blank=True)
    advescrita = models.BooleanField(default=False, null=True, blank=True)
    afastamento = models.BooleanField(default=False, null=True, blank=True)
    cancelmatricula = models.BooleanField(default=False, null=True, blank=True)
    fiap = models.ForeignKey(Fiap, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Observacao(models.Model):
    observacao = models.CharField(max_length=500)
    fiap = models.ForeignKey(Fiap, on_delete=models.CASCADE)
    data = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.id)


class Empresa(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)


class Importancia(models.Model):
    nivel = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)

class Satisfacao(models.Model):
    nivel = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)


class Pergunta(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

class Formulario(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    importancia = models.ForeignKey(Importancia, on_delete=models.CASCADE)
    satisfacao = models.ForeignKey(Satisfacao, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)


class uploadCsv(models.Model):
    File = models.FileField(null=True, upload_to='imports/%y/%m/%d/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.File.path)
        self.importAlunos()

    def importAlunos(self):
        # f = open(self.File.path, "r")
        # print(f.read())

        data = pd.read_excel(self.File.path)

        for row in range(data.shape[0]):
            aluno = Aluno()
            aluno.nome = data.iat[row, 0]
            aluno.ra = data.iat[row, 1]
            aluno.cpf = data.iat[row, 2]
            aluno.turma = Turma.objects.get(cod_turma=data.iat[row, 3])
            aluno.save()

    def __str__(self):
        return str(self.File)