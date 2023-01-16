
from django.core.files.base import ContentFile
from email import message
import json
from pickle import FALSE
from django.db.models.expressions import Case, When
from numpy import False_
from rest_framework import pagination
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from itertools import chain
from django.db.models.aggregates import Count, Sum
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.db.models import Q
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from django.http import Http404, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import ArticleSerializer, EditionSerializer, JournalSerializer
from .models import Journal, Edition, Article
from rest_framework import filters
from datetime import date, datetime
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import jwt
from fullbright.settings import SIMPLE_JWT
from users.serializers import *
from rest_framework import permissions
import pandas as pd
from datetime import date, datetime, time, timedelta
from collections import OrderedDict


class JournalPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST', 'GET'] and request.user.groups.filter(name="Voir journal").exists():
            return True
        if request.method in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE'] and request.user.groups.filter(name="Modifier journal").exists():
            return True
        return False


class AfficheurPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST', 'GET'] and request.user.groups.filter(name="Voir afficheur").exists():
            return True
        if request.method in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE'] and request.user.groups.filter(name="Modifier afficheur").exists():
            return True
        return False


class AnnonceurPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST', 'GET'] and request.user.groups.filter(name="Voir annonceur").exists():
            return True
        if request.method in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE'] and request.user.groups.filter(name="Modifier annonceur").exists():
            return True
        return False


class ChainePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST', 'GET'] and request.user.groups.filter(name="Voir chaine").exists():
            return True
        if request.method in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE'] and request.user.groups.filter(name="Modifier chaine").exists():
            return True
        return False


class RadioPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST', 'GET'] and request.user.groups.filter(name="Voir radio").exists():
            return True
        if request.method in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE'] and request.user.groups.filter(name="Modifier radio").exists():
            return True
        return False


class MyPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class JournalViewTest(generics.ListCreateAPIView):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class JournalView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    pagination_class = MyPagination

    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class JournalClientView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class UpdateJournalView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    lookup_fields = ['pk']


class Journalsearch(generics.ListAPIView):
    # queryset = Journal.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = JournalSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('nomJournal')
        queryset = Journal.objects.filter(nomJournal=nom)
        return queryset


# ---------------------------------------------------------------------------------------------


class EditionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    serializer_class = EditionSerializer

    def get_queryset(self):
        j = self.request.query_params.get('journal')
        queryset = Edition.objects.filter(journal=j).order_by('-date')
        return queryset
# ---------------------------------------------------------------------------------------------


class EditionSearch(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    serializer_class = EditionSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        journal = self.request.query_params.get('journal')
        qset = Edition.objects.filter(journal=journal).order_by('-date')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        querySet = [edition for edition in qset
                    if edition.date >= datetime.strptime(start, '%Y-%m-%d').date()
                    and edition.date <= datetime.strptime(end, '%Y-%m-%d').date()]
        return querySet


class EditionSearchClient(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditionSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        journal = self.request.query_params.get('journal')
        qset = Edition.objects.filter(journal=journal).order_by('-date')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        querySet = [edition for edition in qset
                    if edition.date >= datetime.strptime(start, '%Y-%m-%d').date()
                    and edition.date <= datetime.strptime(end, '%Y-%m-%d').date()]
        return querySet
# ---------------------------------------------------------------------------------------------


class UpdateEditioneView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer


class Editioncount(generics.ListAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    serializer_class = EditionSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('journal')
        queryset = Edition.objects.filter(journal=nom)
        return queryset

# ---------------------------------------------------------------------------------------------


class ArticleView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        edition = self.request.query_params.get('edition')
        queryset = Article.objects.filter(
            edition=edition, confirmed=True)
        return queryset


class PostArticleView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    serializer_class = ArticleSerializer

    def post(self, request, format=None):
        data = request.data
        code = ""
        count = Article.objects.filter(
            edition__date=date.today()).values_list('code', flat=True).distinct().count()
        code = date.today().strftime("%d%m%Y") + "-" + "JR" + "-" + \
            "{0:0=3d}".format(count+1) + "-" + "AR"
        _mutable = data._mutable

        # set to mutable
        data._mutable = True

        # set mutable flag back
        data['code'] = code
        data['confirmed'] = True
        data._mutable = _mutable
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleConfirmed(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ArticleSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        queryset = Article.objects.filter(
            confirmed=False)
        return queryset


class ArticleConfirmedCount(APIView):
    permission_classes = [IsAuthenticated & JournalPermissions & IsAdminUser]

    def get(self, request, format=None):
        count = Article.objects.filter(
            confirmed=False).count()

        return Response(count)


class UpdateArticleView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_fields = ['pk']


class Articlesearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated & JournalPermissions]
    serializer_class = ArticleSerializer

    def get(self, request, format=None):
        jr = self.request.query_params.get('jr')
        edts = Edition.objects.filter(journal=jr).annotate(
            num_article=Count('article', filter=Q(article__confirmed=True))).aggregate(Sum("num_article"))

        if not edts['num_article__sum']:
            edts['num_article__sum'] = 0

        return Response({"nbjr": edts['num_article__sum']})


class SearchFilter(generics.ListAPIView):
    # permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = ArticleSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        langue = self.request.query_params.get('langue')
        debut = self.request.query_params.get('debut')
        fin = self.request.query_params.get('fin')

        accroche = self.request.query_params.get('accroche')
        annonceur = self.request.query_params.get('annonceur')
        marque = self.request.query_params.get('marque')
        produit = self.request.query_params.get('produit')
        edition = self.request.query_params.get('edition')
        type = self.request.query_params.get('type')

        if(annonceur and not marque and not produit):
            queryset = Article.objects.filter(
                accroche__icontains=accroche,
                edition__journal__langue__icontains=langue,
                annonceur=annonceur,
                edition=edition,
                type=type,
                confirmed=True
            )

        elif(annonceur and marque and not produit):
            queryset = Article.objects.filter(
                edition__journal__langue__icontains=langue,

                accroche__icontains=accroche,
                annonceur=annonceur,
                marque=marque,
                edition=edition,
                type=type,

                confirmed=True
            )
        elif(annonceur and marque and produit):
            queryset = Article.objects.filter(
                edition__journal__langue__icontains=langue,

                accroche__icontains=accroche,
                annonceur=annonceur,
                marque=marque,
                produit=produit,
                edition=edition,
                type=type,

                confirmed=True
            )
        elif(not annonceur and not marque and not produit):
            queryset = Article.objects.filter(
                edition__journal__langue__icontains=langue,

                accroche__icontains=accroche,
                edition=edition,
                type=type,
                confirmed=True)

        if(debut != None and fin != None):
            queryset = Article.objects.filter(

                edition__date__range=(datetime.strptime(
                    debut, '%Y-%m-%d'), datetime.strptime(fin, '%Y-%m-%d')),
            )

        return queryset


# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------


class JourAfficheurView(generics.ListCreateAPIView):
    serializer_class = JourAfficheurSerializer
    permission_classes = [IsAuthenticated & AfficheurPermissions]

    def get_queryset(self):
        queryset = JourAfficheur.objects.all()
        return queryset


class JourAfficheurDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    queryset = JourAfficheur.objects.all()
    serializer_class = JourAfficheurSerializer
    lookup_fields = ['pk']


# API pour la table Afficheur :
# AfficheurView : pour  la recuperation de la table entiere.
# AfficheurDetail : pour get,update,delete pour les instances
class AfficheurView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    queryset = Afficheur.objects.all()
    serializer_class = AfficheurSerializer
# ---------------------------------------------------------------------------------------------


class AfficheurDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    queryset = Afficheur.objects.all()
    serializer_class = AfficheurSerializer
    lookup_fields = ['pk']


class Afficheursearch(generics.ListAPIView):
    serializer_class = AfficheurSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('nom_afficheur')
        if nom == None:
            return Afficheur.objects.all()
        queryset = Afficheur.objects.filter(nom_afficheur=nom)
        return queryset


# ---------------------------------------------------------------------------------------------
class getAfficheurInfo(generics.ListAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    pagination_class = MyPagination
    serializer_class = AfficheurSerializer
    queryset = Afficheur.objects.all()


# ---------------------------------------------------------------------------------------------

# API pour la table Panneau :
# PanneauView : pour  la recuperation de la table entiere.
# PanneauDetail : pour get,update,delete pour les instances

class PanneauView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    serializer_class = PanneauSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        nom = self.request.query_params.get('afficheur')
        queryset = Panneau.objects.filter(afficheur=nom).order_by("code")
        return queryset


class PanneauDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    queryset = Panneau.objects.all()
    serializer_class = PanneauSerializer
    lookup_fields = ['pk']


class PanneauFilter(generics.ListAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    serializer_class = PanneauSerializer

    def get_queryset(self):
        afficheur = self.request.query_params.get('afficheur')
        queryset = Panneau.objects.filter(
            afficheur=afficheur)
        return queryset
# ---------------------------------------------------------------------------------------------

# API pour la table Pub :
# PubView : pour  la recuperation de la table entiere.
# PubView : pour get,update,delete pour les instances


class PubViewFalse(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    serializer_class = PubSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('panneau')
        jour = self.request.query_params.get('jour')

        queryset = Pub.objects.filter(
            panneau=nom, jour=jour, confirmed=True, circulation=False)
        return queryset


class PubViewTrue(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    serializer_class = PubSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('panneau')
        jour = self.request.query_params.get('jour')
        queryset = Pub.objects.filter(
            panneau=nom, jour=jour, confirmed=True, circulation=True)
        return queryset


class PubCount(APIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]

    def get(self, request, format=None):
        nom = self.request.query_params.get('panneau')
        jour = self.request.query_params.get('jour')
        countF = Pub.objects.filter(
            panneau=nom, circulation=False, jour=jour).count()
        countT = Pub.objects.filter(
            panneau=nom, circulation=True, jour=jour).count()
        count = {"countF": countF, "countT": countT}
        return Response(count)


class PubDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    queryset = Pub.objects.all()
    serializer_class = PubSerializer
    lookup_fields = ['pk']


class PubConfirmation(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PubSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        queryset = Pub.objects.filter(confirmed=False)
        return queryset


class PubConfirmedCount(APIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]

    def get(self, request, format=None):
        count = Pub.objects.filter(
            confirmed=False).count()

        return Response(count)


class PubFilter(generics.ListAPIView):
    permission_classes = [IsAuthenticated & AfficheurPermissions]
    serializer_class = PubSerializer

    def get_queryset(self):
        code = self.request.query_params.get('code')
        type = self.request.query_params.get('type')

        queryset = []

        if type == 'Sucette dynamique':
            queryset = Pub.objects.filter(code=code, panneau__type=type)
        else:
            queryset = Pub.objects.filter(code=code).exclude(
                panneau__type='Sucette dynamique')

        return queryset


class PubCodes(APIView):
    # permission_classes = [IsAuthenticated & AfficheurPermissions]

    def get(self, request, format=None):
        codes = Pub.objects.filter(confirmed=True).values_list(
            'code', flat=True).distinct()
        return Response(codes)

# --------------------------------------------------------------------------------------


class AnnonceurView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    queryset = Annonceur.objects.all()
    pagination_class = MyPagination
    serializer_class = AnnonceurSerializer


class GetAnnonceurs(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Annonceur.objects.all().order_by("Nom")
    serializer_class = AnnonceurSerializer


class AnnonceurDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    queryset = Annonceur.objects.all()
    serializer_class = AnnonceurSerializer
    lookup_fields = ['pk']


class AnnonceurExiste(APIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]

    def get(self, request, format=None):
        nom = self.request.query_params.get('annonceur')
        bool = Annonceur.objects.filter(Nom=nom).exists()
        return Response(bool)


class Annonceursearch(generics.ListAPIView):
    serializer_class = AnnonceurSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('Nom')
        if nom == None:
            return Annonceur.objects.all()
        queryset = Annonceur.objects.filter(Nom=nom)
        return queryset


class SegmentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = SegmentSerializer
    pagination_class = MyPagination
    queryset = Segment.objects.all()


class GetSegmentsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = SegmentSerializer
    queryset = Segment.objects.all()


class SegmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer
    lookup_fields = ['pk']

############################################################


class MarcheView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = MarcheSerializer
    pagination_class = MyPagination
    queryset = Marche.objects.all()


class GetMarchesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = MarcheSerializer
    queryset = Marche.objects.all()


class MarcheDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    queryset = Marche.objects.all()
    serializer_class = MarcheSerializer
    lookup_fields = ['pk']

############################################################


class FamilleView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = FamilleSerializer
    pagination_class = MyPagination
    queryset = Famille.objects.all()


class GetFamillesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = FamilleSerializer
    queryset = Famille.objects.all()


class FamilleDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    queryset = Famille.objects.all()
    serializer_class = FamilleSerializer
    lookup_fields = ['pk']

############################################################


class SecteurView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = SecteurSerializer
    pagination_class = MyPagination
    queryset = Secteur.objects.all()


class GetSecteursView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SecteurSerializer
    queryset = Secteur.objects.all()


class SecteurDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    queryset = Secteur.objects.all()
    serializer_class = SecteurSerializer
    lookup_fields = ['pk']

############################################################


class GetMarques(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Marque.objects.all().order_by("Nom")
    serializer_class = MarqueSerializer


class MarqueView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = MarqueSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        nom = self.request.query_params.get('annonceur')
        queryset = Marque.objects.filter(NomAnnonceur=nom)
        return queryset


class MarqueDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer
    lookup_fields = ['pk']


class MarqueExiste(APIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]

    def get(self, request, format=None):
        nom = self.request.query_params.get('marque')
        bool = Marque.objects.filter(Nom=nom).exists()
        return Response(bool)


class MarqueInfo(APIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]

    def get(self, request, format=None):
        nom = self.request.query_params.get('marque')
        qs = Publicite.objects.filter(marque=nom)

        response = {}

        if qs.exists():
            qs = qs[0]

            marque = ''
            produit = ''
            segment = ''
            marche = ''
            famille = ''
            secteur = ''

            if(qs.marque):
                marque = qs.marque.id

            if(qs.produit):
                produit = qs.produit.id

            if(qs.segment):
                segment = qs.segment.id

            if(qs.marche):
                marche = qs.marche.id

            if(qs.famille):
                famille = qs.famille.id

            if(qs.secteur):
                secteur = qs.secteur.id

            response = {
                "annonceur": qs.annonceur.id,
                "marque": marque,
                "segment": segment,
                "secteur": secteur,
                "famille": famille,
                "marche": marche,
            }
        return Response(response)


class MarqueSearch(generics.ListAPIView):
    serializer_class = MarqueSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('Nom')
        nomAnn = self.request.query_params.get('annonceur')
        if nom == None:
            return Marque.objects.filter(NomAnnonceur=nomAnn)
        queryset = Marque.objects.filter(Nom=nom)
        return queryset


class MarqueSearchContract(generics.ListCreateAPIView):
    serializer_class = MarqueSerializer
    queryset = Marque.objects.all()

    def post(self):
        nomAnn = self.request.query_params.get('NomAnnonceur')
        queryset = Marque.objects.filter(NomAnnonceur__in=nomAnn)
        return queryset


class GetProduits(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Produit.objects.all().order_by("Nom")
    serializer_class = ProduitSerializer


class ProduitView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = ProduitSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        nom = self.request.query_params.get('marque')
        queryset = Produit.objects.filter(NomMarque=nom)
        return queryset


class ProduitDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    lookup_fields = ['pk']


class ProduitExiste(APIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]

    def get(self, request, format=None):
        nom = self.request.query_params.get('produit')
        bool = Produit.objects.filter(Nom=nom).exists()
        return Response(bool)


class ProduitSearch(generics.ListAPIView):
    serializer_class = ProduitSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('Nom')
        nomM = self.request.query_params.get('marque')
        if nom == None:
            return Produit.objects.filter(NomMarque=nomM)
        queryset = Produit.objects.filter(Nom=nom)
        return queryset
# --------------------------------------------------------------------------------------------------


class AbonnementView(generics.ListCreateAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer


class AbonnementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer
    lookup_fields = ['pk']


class Abonnementsearch(generics.ListAPIView):
    serializer_class = AbonnementSerializer

    def get_queryset(self):
        abn = self.request.query_params.get('client')
        queryset = Abonnement.objects.filter(client=abn)
        return queryset


class WilayaView(generics.ListCreateAPIView):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer


class ApcView(generics.ListCreateAPIView):
    queryset = Apc.objects.all()
    serializer_class = ApcSerializer


class CommunView(generics.ListCreateAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer


# --------------------------------------------------------------------------------------------------


class ContractView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractPost(generics.CreateAPIView):
    queryset = Contract.objects.all()

    def post(self, request):
        ok = {
            "abonnement": request.query_params.get('abonnement'),
            "produits": list(map(int, request.query_params.getlist('produit[]'))),
            "annonceurs": list(map(int, request.query_params.getlist('annonceur[]'))),
            "marques": list(map(int, request.query_params.getlist('marque[]'))),
            "date_debut": request.query_params.get('date_debut'),
            "date_fin": request.query_params.get('date_fin')
        }
        serializer = ContractSerializerPost(data=ok)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    lookup_fields = ['pk']


class Contractsearch(generics.ListAPIView):
    serializer_class = ContractSerializer

    def get_queryset(self):
        ctr = self.request.query_params.get('abonnement')
        queryset = Contract.objects.filter(abonnement=ctr)
        return queryset

# --------------------------------------------------------------------------------------------------


class MarqueFilter(generics.ListAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = MarqueSerializer

    def get_queryset(self):
        NomAnnonceur = self.request.query_params.get('NomAnnonceur')
        queryset = Marque.objects.filter(NomAnnonceur=NomAnnonceur)
        return queryset


class MarqueFilterForContract(generics.ListAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = MarqueSerializer

    def get_queryset(self):
        NomAnnonceur = self.request.query_params.getlist('NomAnnonceur[]')
        queryset = Marque.objects.filter(
            NomAnnonceur__in=NomAnnonceur).order_by("Nom")
        return queryset


class ProduitFilter(generics.ListAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = ProduitSerializer

    def get_queryset(self):
        NomMarque = self.request.query_params.get('NomMarque')
        queryset = Produit.objects.filter(NomMarque=NomMarque)
        return queryset


class ProduitFilterForContract(generics.ListAPIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]
    serializer_class = ProduitSerializer

    def get_queryset(self):
        NomMarque = self.request.query_params.getlist('NomMarque[]')
        queryset = Produit.objects.filter(
            NomMarque__in=NomMarque).order_by("Nom")
        return queryset


class WilayaView(generics.ListCreateAPIView):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer

# --------------------------------------------------------------------------------------------------


class ApcView(generics.ListCreateAPIView):
    queryset = Apc.objects.all()
    serializer_class = ApcSerializer


class Apcsearch(generics.ListAPIView):
    serializer_class = ApcSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('commune')
        queryset = Apc.objects.filter(commune=nom)
        return queryset
# --------------------------------------------------------------------------------------------------


class CommuneView(generics.ListCreateAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer


class Communesearch(generics.ListAPIView):
    serializer_class = CommuneSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('wilaya')
        queryset = Commune.objects.filter(Wilaya=nom)
        return queryset


class getProduitMarqueAnnonceur(APIView):
    permission_classes = [IsAuthenticated & AnnonceurPermissions]

    def get(self, request, format=None):
        produitId = self.request.query_params.get('produit')
        produit = Produit.objects.filter(id=produitId)
        marque = Marque.objects.filter(id=produit[0].NomMarque.id)
        annonceur = Annonceur.objects.filter(id=marque[0].NomAnnonceur.id)

        data = {
            "produit": produit[0].Nom,
            "marque": marque[0].Nom,
            "annonceur": annonceur[0].Nom
        }

        return Response(data)


class ArticleClientView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleClientSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        accroche = self.request.query_params.get('accroche')
        langue = self.request.query_params.get('langue')
        annonceur1 = self.request.query_params.get('annonceur')
        marque1 = self.request.query_params.get('marque')
        produit1 = self.request.query_params.get('produit')
        edition = self.request.query_params.get('edition')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        type = self.request.query_params.get('type')

        if(type == "true"):
            type = True
        else:
            type = False

        if self.request.user.is_client == True:
            qs = Article.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'J':
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.article_set.all()
                                        qs = qs | marque.article_set.filter(
                                            produit=None)
                                    else:
                                        qs = qs | marque.article_set.all()

                                    qs = qs | annonceur.article_set.filter(
                                        marque=None)
                            else:
                                qs = qs | annonceur.article_set.all()

            if(type):

                queryset = qs.filter(
                    type=type,
                    accroche__icontains=accroche,
                    edition__journal__langue__icontains=langue,
                    confirmed=True
                )
            else:
                queryset = qs.filter(
                    accroche__icontains=accroche,
                    edition__journal__langue__icontains=langue,
                    confirmed=True
                )
            if(annonceur1):
                queryset = queryset.filter(
                    annonceur=annonceur1
                )
            if(marque1):
                queryset = queryset.filter(
                    marque=marque1
                )
            if(produit1):
                queryset = queryset.filter(
                    produit=produit1
                )

            articles = Article.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'J':
                    for contract in abonnement.contract_set.all():
                        articles = articles | queryset.filter(edition__date__range=(datetime.strptime(
                            start, '%Y-%m-%d'), datetime.strptime(end, '%Y-%m-%d'))).filter(
                            edition__date__range=(contract.date_debut, contract.date_fin))
            articles = articles.filter(edition=edition)

            return articles


class PubClientView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PubClientSerializer
    pagination_class = MyPagination

    def get_queryset(self):

        accroche = self.request.query_params.get('accroche')
        langue = self.request.query_params.get('langue')
        annonceur1 = self.request.query_params.get('annonceur')
        marque1 = self.request.query_params.get('marque')
        produit1 = self.request.query_params.get('produit')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if self.request.user.is_client == True:
            qs = Pub.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'P':
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.pub_set.all()
                                        qs = qs | marque.pub_set.filter(
                                            produit=None)
                                    else:
                                        qs = qs | marque.pub_set.all()
                                    qs = qs | marque.pub_set.filter(
                                        marque=None)
                            else:
                                qs = qs | annonceur.pub_set.all()
            queryset = qs.filter(
                accroche__icontains=accroche,
                langue__icontains=langue,
                confirmed=True
            )
            if(annonceur1):
                queryset = queryset.filter(
                    annonceur=annonceur1
                )
            if(marque1):
                queryset = queryset.filter(
                    marque=marque1
                )
            if(produit1):
                queryset = queryset.filter(
                    produit=produit1
                )

            pubs = Pub.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'P':
                    for contract in abonnement.contract_set.all():
                        pubs = pubs | queryset.filter(date_creation__range=(datetime.strptime(
                            start, '%Y-%m-%d'), datetime.strptime(end, '%Y-%m-%d'))).filter(
                            date_creation__range=(contract.date_debut, contract.date_fin))

            return pubs


class ClientAbonnement(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AbonnementSerializer

    def get_queryset(self):
        if self.request.user.is_client == True:
            return self.request.user.abonnement_set.all()


class ContractViewClient(generics.ListCreateAPIView):
    serializer_class = ContractSerializer

    def get_queryset(self):
        return Contract.objects.filter(
            abonnement=self.request.query_params.get('abonnoment'))


class VideoConfirmedCount(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        count = Publicite.objects.filter(
            confirmed=False).count()
        return Response(count)


class VideoConfirmation(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Publicite.objects.all()
    serializer_class = PubliciteSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        return Publicite.objects.filter(confirmed=False)


class ChaineView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = Chaine.objects.all().order_by("nom")
    serializer_class = ChaineSerializer
    pagination_class = MyPagination


class ChaineAllView(generics.ListAPIView):
    queryset = Chaine.objects.all().order_by("nom")
    serializer_class = ChaineSerializer


class ChaineDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = Chaine.objects.all()
    serializer_class = ChaineSerializer
    lookup_fields = ['pk']


class Chainesearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    serializer_class = ChaineSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('nom')
        if nom == None:
            return Chaine.objects.all()
        queryset = Chaine.objects.filter(nom=nom)

        return queryset


class ArticleLinkClient(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleClientSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        if self.request.user.is_client == True:
            qs = Article.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "J":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.article_set.all()
                                    else:
                                        qs = qs | marque.article_set.all()
                            else:
                                qs = qs | annonceur.article_set.all()
            return qs.filter(id=id)


class PubLinkClient(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pub.objects.all()
    serializer_class = PubClientSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        if self.request.user.is_client == True:
            qs = Pub.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "P":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.pub_set.all()
                                    else:
                                        qs = qs | marque.pub_set.all()
                            else:
                                qs = qs | annonceur.pub_set.all()
            return qs.filter(id=id)


class PubliciteLinkClient(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Publicite.objects.all()
    serializer_class = PubliciteSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        if self.request.user.is_client == True:
            qs = Pub.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "C":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.publicite_set.all()
                                    else:
                                        qs = qs | marque.publicite_set.all()
                            else:
                                qs = qs | annonceur.publicite_set.all()

            return qs.filter(id=id)


class send_email(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):

        clients = User.objects.filter(is_client=True, is_active=True)
        jours = Jour.objects.filter(date=date.today())

        for client in clients:

            qs = Article.objects.none()
            for abonnement in client.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'J':
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.article_set.filter(
                                                date_creation=date.today())
                                    else:
                                        qs = qs | marque.article_set.filter(
                                            date_creation=date.today())
                            else:
                                qs = qs | annonceur.article_set.filter(
                                    date_creation=date.today())

            qsVid = Publicite.objects.none()
            for abonnement in client.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'C':
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qsVid = qsVid | produit.publicite_set.filter(
                                                jour__in=jours)
                                    else:
                                        qsVid = qsVid | marque.publicite_set.filter(
                                            jour__in=jours)
                            else:
                                qsVid = qsVid | annonceur.publicite_set.filter(
                                    jour__in=jours)

            list_dic = []

            for article in qs:
                acc = ""
                if len(article.accroche) > 70:
                    acc = article.accroche[:70]+" ..."
                else:
                    acc = article.accroche

                list_dic.append({
                    "media": "Journal",
                    "support": article.edition.journal.nomJournal,
                    "accroche": acc,
                    "date": article.date_creation,
                    "annonceur": article.annonceur.Nom,
                    "marque": article.marque.Nom if article.marque else '/',
                    "produit": article.produit.Nom if article.produit else '/',
                    "lien": "http://client.promediaconseils.com/article/link/"+str(article.id)
                })

            for article in qsVid:
                acc = ""
                if len(article.message) > 70:
                    acc = article.message[:70]+" ..."
                else:
                    acc = article.message

                list_dic.append({
                    "media": "TV",
                    "support": article.jour.chaine.nom,
                    "accroche": acc,
                    "date": article.jour.date,
                    "annonceur": article.annonceur.Nom,
                    "marque": article.marque.Nom if article.marque else '/',
                    "produit": article.produit.Nom if article.produit else '/',
                    "lien": "http://client.promediaconseils.com/pub/link/"+str(article.id)
                })

            list_dic = sorted(list_dic, key=lambda x: x['annonceur'])

            emailm = """
        <!DOCTYPE html>
<html>
	<table style="border-collapse: collapse;
	margin: 25px 0;
	font-size: 0.9em;
	min-width: 400px;
	border-radius: 5px 5px 0 0;
	overflow: hidden;
	box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);width: 100%;font-family: sans-serif;" >
		<thead style="background-color: #0070f3;
		color: #ffffff;
		text-align: left;
		font-weight: bold;">
			<tr style="background-color: #0070f3;
			color: #ffffff;
			text-align: left;
			font-weight: bold;">
				<th style="padding: 12px 15px;">Media</th>
				<th style="padding: 12px 15px;">Support</th>
				<th style="padding: 12px 15px;">Accroche</th>
				<th style="padding: 12px 15px;">Date</th>
				<th style="padding: 12px 15px;">Annonceur</th>
				<th style="padding: 12px 15px;">Marque</th>
				<th style="padding: 12px 15px;">Produit</th>
				<th style="padding: 12px 15px;">Lien</th>
			</tr>
		</thead>
		<tbody style="border-bottom: 1px solid #dddddd;">


        """

            for item in list_dic:

                emailm = emailm+"""
                <tr style="border-bottom: 1px solid #dddddd;color="black">
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td>
                        <div style="
                        overflow: hidden;
                        text-overflow: ellipsis;
                        display: -webkit-box;
                        -webkit-line-clamp: 1; /* number of lines to show */
                                line-clamp: 1;
                        -webkit-box-orient: vertical;" >
                            {}
                        </div>
                    </td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">
                        <button style="
                        border: none;
                        padding: 0 10px;
                        height: 35px;
                        line-height: 25px;
                        border-radius: 7px;
                        background-color: #0070f3;
                        color: white;

                            ">
                            <a style="color: white;
                            text-decoration: none;" href="{} ">
                                lien
                            </a>
                        </button>
                    </td>

                </tr>

                """.format(item["media"], item["support"], item["accroche"], item["date"], item["annonceur"], item["marque"], item["produit"], item["lien"])

            emailm = emailm + """</tbody>
                                    </table>
                                </html>"""

            if len(qs) != 0:
                email = EmailMessage(
                    # 'A new mail from ProMediaConseils!', emailm, to=[client.email])
                    'A new mail from ProMediaConseils!', emailm, to=["ghecharaf@gmail.com"])
                email.content_subtype = "html"
                email.send()
        return Response("ok")
# 'fayssalbenaissa1513@gmail.com'


class send_email_chaine(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):

        clients = User.objects.filter(is_client=True, is_active=True)
        jours = Jour.objects.filter(date=date.today())

        for client in clients:

            qs = Publicite.objects.none()
            for abonnement in client.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'C':
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.publicite_set.filter(
                                                jour__in=jours)
                                    else:
                                        qs = qs | marque.publicite_set.filter(
                                            jour__in=jours)
                            else:
                                qs = qs | annonceur.publicite_set.filter(
                                    jour__in=jours)

            emailm = """
        <!DOCTYPE html>
<html>
	<table style="border-collapse: collapse;
	margin: 25px 0;
	font-size: 0.9em;
	min-width: 400px;
	border-radius: 5px 5px 0 0;
	overflow: hidden;
	box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);width: 100%;font-family: sans-serif;" >
		<thead style="background-color: #0070f3;
		color: #ffffff;
		text-align: left;
		font-weight: bold;">
			<tr style="background-color: #0070f3;
			color: #ffffff;
			text-align: left;
			font-weight: bold;">
				<th style="padding: 12px 15px;">Chaine</th>
				<th style="padding: 12px 15px;">Message</th>
				<th style="padding: 12px 15px;">Date</th>
				<th style="padding: 12px 15px;">Annonceur</th>
				<th style="padding: 12px 15px;">Marque</th>
				<th style="padding: 12px 15px;">Produit</th>
				<th style="padding: 12px 15px;">Lien</th>
			</tr>
		</thead>
		<tbody style="border-bottom: 1px solid #dddddd;">


        """
            for article in qs:
                acc = ""
                if len(article.message) > 70:
                    acc = article.message[:70]+" ..."
                else:
                    acc = article.message
                emailm = emailm+"""
                <tr style="border-bottom: 1px solid #dddddd;color="black">
                    <td style="padding: 12px 15px;">{}</td>
                    <td>
                        <div style="
                        overflow: hidden;
                        text-overflow: ellipsis;
                        display: -webkit-box;
                        -webkit-line-clamp: 1; /* number of lines to show */
                                line-clamp: 1;
                        -webkit-box-orient: vertical;" >
                            {}
                        </div>
                    </td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">{}</td>
                    <td style="padding: 12px 15px;">
                        <button style="
                        border: none;
                        padding: 0 10px;
                        height: 35px;
                        line-height: 25px;
                        border-radius: 7px;
                        background-color: #0070f3;
                        color: white;

                            ">
                            <a style="color: white;
                            text-decoration: none;" href="{} ">
                                lien
                            </a>
                        </button>
                    </td>

                </tr>

                """.format(article.jour.chaine.nom, acc, article.jour.date, article.annonceur.Nom, article.marque.Nom if article.marque else '', article.produit.Nom if article.produit else '', "http://client.promediaconseils.com/pub/link/"+str(article.id))

            emailm = emailm + """</tbody>
                                    </table>
                                </html>"""

            if len(qs) != 0:
                email = EmailMessage(
                    'A new mail from ProMediaConseils!', emailm, to=["ghecharaf@gmail.com"])
                email.content_subtype = "html"
                email.send()
        return Response("ok")


class PubliciteView(generics.ListCreateAPIView):
    serializer_class = PubliciteSerializer
    queryset = Publicite.objects.all()
    permission_classes = [IsAuthenticated & ChainePermissions]


class GetMessagesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PubliciteSerializer

    def get_queryset(self):
        type = self.request.query_params.get('type')
        msg = self.request.query_params.get('message')

        msgs = []
        result = []

        if type == '0':

            queryset = Publicite.objects.all()

            for item in queryset:
                if item.message not in msgs:
                    msgs.append(item.message)
                    result.append(item)

        if type == '1':
            queryset = Publicite.objects.filter(message__icontains=msg)

            for item in queryset:
                if item.message not in msgs:
                    result.append(item)
                    msgs.append(item.message)

        return result


class RecherchePublicite(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PubliciteSerializer

    def get_queryset(self):
        type = self.request.query_params.get('type')
        msg = self.request.query_params.get('message')

        msgs = []
        result = []

        if type == '0':

            queryset = Publicite.objects.all()

            for item in queryset:
                if item.message not in msgs:
                    msgs.append(item.message)
                    result.append(item)

        if type == '1':
            queryset = Publicite.objects.filter(
                message__icontains=msg).order_by("-id")

            for item in queryset:
                if item.message not in msgs:
                    result.append(item)
                    msgs.append(item.message)

        if type == 2:
            result = Publicite.objects.filter(message__icontains=msg)

        return result


class PostPubliciteView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    serializer_class = PubliciteSerializer

    def post(self, request, format=None):
        data = request.data
        code = ""
        jours = Jour.objects.filter(date=date.today())

        count = Publicite.objects.filter(
            jour__in=jours).values_list('code', flat=True).distinct().count()
        code = date.today().strftime("%d%m%Y") + "-" + "TV" + "-" + \
            "{0:0=3d}".format(count+1) + "-" + data['language']
        data['code'] = code
        data['confirmed'] = True
        if len(data['video'].name) >= 100:
            data['video'].name = data['video'].name[:50]

        serializer = PubliciteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostPubliciteExisteView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    serializer_class = PubliciteSerializer

    def post(self, request, format=None):
        id = request.data['id']
        jour = request.data['jour']
        data = request.data
        video = Publicite.objects.filter(id=id)[0]

        jours = Jour.objects.filter(date=date.today())

        code = ""

        count = Publicite.objects.filter(
            jour__in=jours).values_list('code', flat=True).distinct().count()
        code = date.today().strftime("%d%m%Y") + "-" + "TV" + "-" + \
            "{0:0=3d}".format(count+1) + "-" + video.language

        _mutable = data._mutable

        # set to mutable
        data._mutable = True

        data['code'] = code
        data['jour'] = jour
        data['confirmed'] = True

        publicite = Publicite.objects.filter(jour=jour)
        programme = Programme.objects.filter(jour=jour)

        response = []
        i = 0
        for prog in programme:
            response.append({
                "annonceur": "-",
                "id": i,
                "message": prog.message,
                "debut": prog.debut,
                "duree": datetime.combine(date.today(), prog.fin) - datetime.combine(date.today(), prog.debut),
                "fin": prog.fin,
                "type": 1,
                "lien": prog.id,
                "ecran": "-"
            })
            i += 1
        for pub in publicite:
            response.append({
                "annonceur": pub.annonceur.Nom,
                "id": i,
                "message": pub.message,
                "debut": pub.debut,
                "duree": datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut),

                "fin": pub.fin,
                "type": 2,
                "lien": pub.id,
                "ecran": pub.ecran
            })
            i += 1
        response = sorted(response, key=lambda d: d['debut'])

        data['debut'] = response[len(response)-1]['fin']
        data['debut'] = datetime.combine(
            date.min, data['debut']) + timedelta(seconds=1)
        data['debut'] = data['debut'].strftime("%H:%M:%S")

        x = datetime.combine(date.min, video.fin) - \
            datetime.combine(date.min, video.debut)

        data['fin'] = datetime.combine(
            date.min, response[len(response)-1]['fin']) + timedelta(seconds=x.seconds+1)

        data['fin'] = data['fin'].strftime("%H:%M:%S")

        picture_copy = ContentFile(video.video.read())
        newname = video.video.name[:50] + \
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if len(newname) >= 100:
            picture_copy.name = newname[:100]
        else:
            picture_copy.name = newname

        data['video'] = picture_copy

        data._mutable = _mutable

        serializer = PubliciteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModifierTempView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = Publicite.objects.all()
    serializer_class = PubliciteSerializer
    lookup_fields = ['pk']


class PubliciteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = Publicite.objects.all()
    serializer_class = PubliciteSerializer
    lookup_fields = ['pk']


class PubliciteClientDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Publicite.objects.all()
    serializer_class = PubliciteSerializer
    lookup_fields = ['pk']


class ProgrammeView(generics.ListCreateAPIView):
    serializer_class = ProgrammeSerializer
    queryset = Programme.objects.all()
    permission_classes = [IsAuthenticated & ChainePermissions]


class UpdateProgrammeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer
    permission_classes = [IsAuthenticated & ChainePermissions]


class JourDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = Jour.objects.all()
    serializer_class = JourSerializer
    lookup_fields = ['pk']


class JourView(generics.ListCreateAPIView):
    serializer_class = JourSerializer
    permission_classes = [IsAuthenticated & ChainePermissions]

    def get_queryset(self):
        id = self.request.query_params.get('id')
        queryset = Jour.objects.filter(chaine=id).order_by('date')
        return queryset


class JourViewClient(generics.ListAPIView):
    serializer_class = JourSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        queryset = Jour.objects.filter(chaine=id).order_by('date')
        return queryset


class ProgrammeEtPub(APIView):
    permission_classes = [IsAuthenticated & ChainePermissions]

    def get(self, request):
        id = self.request.query_params.get('id')
        publicite = Publicite.objects.filter(jour=id, confirmed=True)
        programme = Programme.objects.filter(jour=id)
        response = []
        i = 0
        for prog in programme:
            response.append({
                "idd": prog.id,
                "annonceur": "-",
                "id": i,
                "message": prog.message,
                "debut": prog.debut,
                "duree": datetime.combine(date.today(), prog.fin) - datetime.combine(date.today(), prog.debut),
                "fin": prog.fin,
                "type": 1,
                "lien": prog.id,
                "ecran": "-"
            })
            i += 1
        for pub in publicite:
            response.append({
                "idd": pub.id,
                "annonceur": pub.annonceur.Nom,
                "id": i,
                "message": pub.message,
                "debut": pub.debut,
                "duree": datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut),

                "fin": pub.fin,
                "type": 2,
                "lien": pub.id,
                "ecran": pub.ecran
            })
            i += 1
        return Response(sorted(response, key=lambda d: d['debut']))


class ChaneiClientView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jour = self.request.query_params.get('id')

        if self.request.user.is_client == True:

            qs = Publicite.objects.none()

            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "C":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):

                                            qs = qs | produit.publicite_set.all()
                                        qs = qs | marque.publicite_set.filter(
                                            produit=None)
                                    else:
                                        qs = qs | marque.publicite_set.all()
                                qs = qs | annonceur.publicite_set.filter(
                                    marque=None)

                            else:
                                qs = qs | annonceur.publicite_set.all()

            queryset = qs.filter(
                confirmed=True
            )
            videos = Publicite.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'C':
                    for contract in abonnement.contract_set.all():
                        if Jour.objects.filter(id=jour, date__range=(contract.date_debut, contract.date_fin)).exists():
                            videos = videos | queryset.filter(jour=jour)

            programme = Programme.objects.none()
            if len(videos):
                programme = Programme.objects.filter(jour=jour)

            response = []
            i = 0
            for prog in programme:
                response.append({
                    "annonceur": '-',
                    "id": i,
                    "message": prog.message,
                    "debut": prog.debut,
                    "duree": datetime.combine(date.today(), prog.fin) - datetime.combine(date.today(), prog.debut),
                    "fin": prog.fin,
                    "type": 1,
                    "lien": prog.id,
                    "ecran": "-"
                })
                i += 1
            for pub in videos:
                response.append({
                    "annonceur": pub.annonceur.Nom,

                    "id": i,
                    "message": pub.message,
                    "debut": pub.debut,
                    "duree": datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut),
                    "fin": pub.fin,
                    "type": 2,
                    "lien": pub.id,
                    "ecran": pub.ecran
                })
                i += 1

            return Response(sorted(response, key=lambda d: d['debut']))


class PubViewTest(APIView):
    # permission_classes = [IsAuthenticated & AfficheurPermissions]
    serializer_class = PubSerializer

    def post(self, request, format=None):
        data = request.data
        code = ""
        if data['code'] == '':
            count = Pub.objects.filter(
                date_creation=date.today()).values_list('code', flat=True).distinct().count()
            code = date.today().strftime("%d%m%Y") + "-" + "AF" + "-" + \
                "{0:0=3d}".format(count+1) + "-" + data['langue']
            data['code'] = code
            data['confirmed'] = True
            serializer = PubSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            _mutable = data._mutable

            # set to mutable
            data._mutable = True
            data['confirmed'] = True
            obj = Pub.objects.filter(code=data['code'])[0]

            if obj.image:
                picture_copy = ContentFile(obj.image.read())
                picture_copy.name = obj.image.name + datetime.now().strftime("%d/%m/%Y-%H:%M:%S") + \
                    '.'+obj.image.name.split('.')[-1]

                data['image'] = picture_copy
            else:
                picture_copy = ContentFile(obj.video.read())
                picture_copy.name = obj.video.name + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                data['video'] = obj.video

            data['date_creation'] = obj.date_creation

            data._mutable = _mutable

            serializer = PubSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# RAdio >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


class SonConfirmedCount(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        count = PubliciteRadio.objects.filter(
            confirmed=False).count()
        return Response(count)


class SonConfirmation(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = PubliciteRadio.objects.all()
    serializer_class = PubliciteRadioSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        return PubliciteRadio.objects.filter(confirmed=False)


class RadioView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & RadioPermissions]
    queryset = Radio.objects.all().order_by("nom")
    serializer_class = RadioSerializer
    pagination_class = MyPagination


class RadioAllView(generics.ListAPIView):
    queryset = Radio.objects.all().order_by("nom")
    serializer_class = RadioSerializer


class RadioDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & RadioPermissions]
    queryset = Radio.objects.all()
    serializer_class = RadioSerializer
    lookup_fields = ['pk']


class Radiosearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated & RadioPermissions]
    serializer_class = RadioSerializer

    def get_queryset(self):
        nom = self.request.query_params.get('nom')
        if nom == None:
            return Radio.objects.all()
        queryset = Radio.objects.filter(nom=nom)

        return queryset


class PubliciteRadioView(generics.ListCreateAPIView):
    serializer_class = PubliciteRadioSerializer
    queryset = PubliciteRadio.objects.all()
    permission_classes = [IsAuthenticated & RadioPermissions]


class PostPubliciteRadioView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & RadioPermissions]
    serializer_class = PubliciteRadioSerializer

    def post(self, request, format=None):
        data = request.data
        code = ""
        jours = JourRadio.objects.filter(date=date.today())

        count = PubliciteRadio.objects.filter(
            jour__in=jours).values_list('code', flat=True).distinct().count()
        code = date.today().strftime("%d%m%Y") + "-" + "RD" + "-" + \
            "{0:0=3d}".format(count+1) + "-" + data['language']
        data['code'] = code
        data['confirmed'] = True
        serializer = PubliciteRadioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PubliciteRadioDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & RadioPermissions]
    queryset = PubliciteRadio.objects.all()
    serializer_class = PubliciteRadioSerializer
    lookup_fields = ['pk']


class PubliciteRadioClientDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PubliciteRadio.objects.all()
    serializer_class = PubliciteRadioSerializer
    lookup_fields = ['pk']


class ProgrammeRadioView(generics.ListCreateAPIView):
    serializer_class = ProgrammeRadioSerializer
    queryset = ProgrammeRadio.objects.all()
    permission_classes = [IsAuthenticated & RadioPermissions]


class UpdateProgrammeRadioView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProgrammeRadio.objects.all()
    serializer_class = ProgrammeRadioSerializer
    permission_classes = [IsAuthenticated & RadioPermissions]


class JourRadioDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & RadioPermissions]
    queryset = JourRadio.objects.all()
    serializer_class = JourRadio
    lookup_fields = ['pk']


class JourRadioView(generics.ListCreateAPIView):
    serializer_class = JourRadioSerializer
    permission_classes = [IsAuthenticated & RadioPermissions]

    def get_queryset(self):
        id = self.request.query_params.get('id')
        queryset = JourRadio.objects.filter(radio=id).order_by('date')
        return queryset


class JourRadioViewClient(generics.ListAPIView):
    serializer_class = JourRadioSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        queryset = JourRadio.objects.filter(radio=id).order_by('date')
        return queryset


class ProgrammeEtPubRadio(APIView):
    permission_classes = [IsAuthenticated & RadioPermissions]

    def get(self, request):
        id = self.request.query_params.get('id')
        publicite = PubliciteRadio.objects.filter(jour=id, confirmed=True)
        programme = ProgrammeRadio.objects.filter(jour=id)
        response = []
        i = 0
        for prog in programme:
            response.append({
                "annonceur": "-",
                "id": i,
                "message": prog.message,
                "debut": prog.debut,
                "duree": datetime.combine(date.today(), prog.fin) - datetime.combine(date.today(), prog.debut),
                "fin": prog.fin,
                "type": 1,
                "lien": prog.id,
                "ecran": "-"
            })
            i += 1
        for pub in publicite:
            response.append({
                "annonceur": pub.annonceur.Nom,
                "id": i,
                "message": pub.message,
                "debut": pub.debut,
                "duree": datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut),

                "fin": pub.fin,
                "type": 2,
                "lien": pub.id,
                "ecran": pub.ecran
            })
            i += 1
        return Response(sorted(response, key=lambda d: d['debut']))


class RadioClientView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jour = self.request.query_params.get('id')

        if self.request.user.is_client == True:

            qs = PubliciteRadio.objects.none()

            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "R":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):

                                            qs = qs | produit.publiciteradio_set.all()
                                        qs = qs | marque.publiciteradio_set.filter(
                                            produit=None)
                                    else:
                                        qs = qs | marque.publiciteradio_set.all()

                                qs = qs | annonceur.publiciteradio_set.filter(
                                    marque=None)

                            else:
                                qs = qs | annonceur.publiciteradio_set.all()

            queryset = qs.filter(
                confirmed=True
            )
            videos = PubliciteRadio.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'C':
                    for contract in abonnement.contract_set.all():
                        if JourRadio.objects.filter(id=jour, date__range=(contract.date_debut, contract.date_fin)).exists():
                            videos = videos | queryset.filter(jour=jour)

            programme = ProgrammeRadio.objects.none()
            if len(videos):
                programme = ProgrammeRadio.objects.filter(jour=jour)

            response = []
            i = 0
            for prog in programme:
                response.append({
                    "annonceur": '-',
                    "id": i,
                    "message": prog.message,
                    "debut": prog.debut,
                    "duree": datetime.combine(date.today(), prog.fin) - datetime.combine(date.today(), prog.debut),
                    "fin": prog.fin,
                    "type": 1,
                    "lien": prog.id,
                    "ecran": "-"
                })
                i += 1
            for pub in videos:
                response.append({
                    "annonceur": pub.annonceur.Nom,

                    "id": i,
                    "message": pub.message,
                    "debut": pub.debut,
                    "duree": datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut),
                    "fin": pub.fin,
                    "type": 2,
                    "lien": pub.id,
                    "ecran": pub.ecran
                })
                i += 1

            return Response(sorted(response, key=lambda d: d['debut']))


class TarifChaineView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = TarifChaine.objects.all()
    serializer_class = TarifChaineSerializer


class TarifChaineDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = TarifChaine.objects.all()
    serializer_class = TarifChaineSerializer
    lookup_fields = ['pk']


class GetTarifChaineView(generics.ListCreateAPIView):
    serializer_class = TarifChaineSerializer
    permission_classes = [IsAuthenticated & ChainePermissions]

    def get_queryset(self):
        id = self.request.query_params.get('id')
        queryset = TarifChaine.objects.filter(chaine=id).order_by('debut')
        return queryset


class IndiceView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = Indice.objects.all()
    serializer_class = IndiceSerializer


class IndiceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & ChainePermissions]
    queryset = Indice.objects.all()
    serializer_class = IndiceSerializer
    lookup_fields = ['pk']


class TarifRadioView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & RadioPermissions]
    queryset = TarifRadio.objects.all()
    serializer_class = TarifRadioSerializer


class TarifRadioDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & RadioPermissions]
    queryset = TarifRadio.objects.all()
    serializer_class = TarifRadioSerializer
    lookup_fields = ['pk']


class GetTarifRadioView(generics.ListCreateAPIView):
    serializer_class = TarifRadioSerializer
    permission_classes = [IsAuthenticated & RadioPermissions]

    def get_queryset(self):
        id = self.request.query_params.get('id')
        queryset = TarifRadio.objects.filter(radio=id).order_by('debut')
        return queryset


class PigeFinaleView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        debut = request.query_params.get('debut'),
        date_fin = request.query_params.get('date_fin')

        if self.request.user.is_client == True:

            qs = Publicite.objects.none()

            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "C":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):

                                            qs = qs | produit.publicite_set.all()
                                        qs = qs | marque.publicite_set.filter(
                                            produit=None)
                                    else:
                                        qs = qs | marque.publicite_set.all()

                                qs = qs | annonceur.publicite_set.filter(
                                    marque=None)

                            else:
                                qs = qs | annonceur.publicite_set.all()

            queryset = qs.filter(
                confirmed=True
            )
            videos = Publicite.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'C':
                    for contract in abonnement.contract_set.all():
                        if timezone.now().date() >= contract.date_debut and timezone.now().date() <= contract.date_fin:
                            jours = Jour.objects.filter(date__range=(
                                debut[0], date_fin))
                            videos = videos | queryset.filter(jour__in=jours)

            response = []
            i = 0
            for pub in videos:
                tarifs = TarifChaine.objects.filter(chaine=pub.jour.chaine)
                indices = Indice.objects.filter(
                    chaine=pub.jour.chaine).order_by("-indice")

                tarif = tarifs.filter(debut__lte=pub.debut, fin__gte=pub.debut)

                duree = datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) if datetime.combine(date.today(), pub.fin) - datetime.combine(
                    date.today(), pub.debut) >= timedelta(seconds=1) else datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) + timedelta(hours=24)
                indice = indices.filter(duree__lte=duree.total_seconds())
                ind = 1

                if len(indice) > 0:
                    ind = indice[len(indice)-1].indice/100

                if(len(tarif) < 1):
                    tarif = ""

                programmeAvant = Programme.objects.filter(
                    jour=pub.jour, fin__lte=pub.debut)
                programmeApres = Programme.objects.filter(
                    jour=pub.jour, debut__gte=pub.fin)

                if(len(programmeAvant) < 1):
                    programmeAvant = Publicite.objects.filter(
                        jour=pub.jour, fin__lte=pub.debut)
                if(len(programmeApres) < 1):
                    programmeApres = Publicite.objects.filter(
                        jour=pub.jour, debut__gte=pub.fin)

                marque = '/'
                produit = '/'
                segment = '/'
                marche = '/'
                famille = '/'
                secteur = '/'

                if(pub.marque):
                    marque = pub.marque.Nom

                if(pub.produit):
                    produit = pub.produit.Nom

                if(pub.segment):
                    segment = pub.segment.Nom

                if(pub.marche):
                    marche = pub.marche.Nom

                if(pub.famille):
                    famille = pub.famille.Nom

                if(pub.secteur):
                    secteur = pub.secteur.Nom

                brut = ((duree*(tarif[0].prix*ind))/30)

                if ind == 0:
                    brut = ((duree*(tarif[0].prix*1))/30)

                response.append({
                    "id": i,
                    'media': 'TV',
                    'date': pub.jour.date,
                    'support': pub.jour.chaine.nom,
                    "debut": pub.debut,
                    "duree": duree,
                    "couleur": '/',
                    "code": pub.code,
                    "message": pub.message,
                    "annonceur": pub.annonceur.Nom,
                    "marque": marque,
                    "produit": produit,
                    "segment": segment,
                    "marche": marche,
                    "famille": famille,
                    "secteur": secteur,
                    "avant": programmeAvant[0].message if len(programmeAvant) > 0 else '/',
                    'apres': programmeApres[len(programmeApres)-1].message if len(programmeApres) > 0 else '/',
                    "ecran": pub.ecran,
                    "afficheur": "/",
                    "panneau": "/",
                    "adresse": "/",
                    "wilaya": "/",
                    "apc": "/",
                    "typeachat": "achat classic",
                    "periodicite": "quotidienne",
                    "mois": "/",
                    "datedebut": "/",
                    "datefin": "/",
                    "nbjour": "/",
                    "langue": "/",
                    'tarifbrut': brut if tarif != '' else '/',
                    'tarifsec': tarif[0].prix if tarif != ''else '/'
                })
                i += 1
            response = sorted(response, key=lambda d: d['debut'])
            response = sorted(response, key=lambda d: d['date'])
            response = sorted(response, key=lambda d: d['support'])

            # Radio
            qs = PubliciteRadio.objects.none()

            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "R":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.publiciteradio_set.all()
                                        qs = qs | marque.publiciteradio_set.filter(
                                            produit=None)
                                    else:
                                        qs = qs | marque.publiciteradio_set.all()

                                qs = qs | annonceur.publiciteradio_set.filter(
                                    marque=None)

                            else:
                                qs = qs | annonceur.publiciteradio_set.all()

            queryset = qs.filter(
                confirmed=True
            )
            videos = PubliciteRadio.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'R':
                    for contract in abonnement.contract_set.all():
                        if timezone.now().date() >= contract.date_debut and timezone.now().date() <= contract.date_fin:
                            jours = JourRadio.objects.filter(date__range=(
                                debut[0], date_fin))
                            videos = videos | queryset.filter(jour__in=jours)

            for pub in videos:
                tarifs = TarifRadio.objects.filter(radio=pub.jour.radio)

                tarif = tarifs.filter(debut__lte=pub.debut, fin__gte=pub.debut)

                if(len(tarif) < 1):
                    tarif = ""

                programmeAvant = ProgrammeRadio.objects.filter(
                    jour=pub.jour, fin__lte=pub.debut)
                programmeApres = ProgrammeRadio.objects.filter(
                    jour=pub.jour, debut__gte=pub.fin)

                if(len(programmeAvant) < 1):
                    programmeAvant = PubliciteRadio.objects.filter(
                        jour=pub.jour, fin__lte=pub.debut)
                if(len(programmeApres) < 1):
                    programmeApres = PubliciteRadio.objects.filter(
                        jour=pub.jour, debut__gte=pub.fin)

                marque = '/'
                produit = '/'
                segment = '/'
                marche = '/'
                famille = '/'
                secteur = '/'

                if(pub.marque):
                    marque = pub.marque.Nom

                if(pub.produit):
                    produit = pub.produit.Nom

                if(pub.segment):
                    segment = pub.segment.Nom

                if(pub.marche):
                    marche = pub.marche.Nom

                if(pub.famille):
                    famille = pub.famille.Nom

                if(pub.secteur):
                    secteur = pub.secteur.Nom

                response.append({
                    "id": i,
                    'media': 'RD',
                    'date': pub.jour.date,
                    'support': pub.jour.radio.nom,
                    "debut": pub.debut,
                    "duree": datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) if datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) >= timedelta(seconds=1) else datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) + timedelta(hours=24),
                    "couleur": '/',
                    "code": pub.code,
                    "message": pub.message,
                    "annonceur": pub.annonceur.Nom,
                    "marque": marque,
                    "produit": produit,
                    "segment": segment,
                    "marche": marche,
                    "famille": famille,
                    "secteur": secteur,
                    "avant": programmeAvant[0].message if len(programmeAvant) > 0 else '/',
                    'apres': programmeApres[len(programmeApres)-1].message if len(programmeApres) > 0 else '/',
                    "ecran": pub.ecran,
                    "afficheur": '/',
                    "panneau": '/',
                    "adresse": '/',
                    "wilaya": '/',
                    "apc": '/',
                    "typeachat": "achat classic",
                    "periodicite": "quotidienne",
                    "mois": "",
                    "datedebut": "",
                    "datefin": "",
                    "nbjour": "",
                    "langue": "",
                    'tarifbrut': ((datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut))*tarif[0].prix/30) if tarif != '' else '/',
                    'tarifsec': tarif[0].prix if tarif != ''else '/'
                })
                i += 1
            response = sorted(response, key=lambda d: d['date'])

            # "# Afficheur
            qs = Pub.objects.none()

            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "P":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.pub_set.all()
                                        qs = qs | marque.pub_set.filter(
                                            produit=None)
                                    else:
                                        qs = qs | marque.pub_set.all()

                                qs = qs | annonceur.pub_set.filter(
                                    marque=None)

                            else:
                                qs = qs | annonceur.pub_set.all()

            queryset = qs.filter(
                confirmed=True
            )
            videos = Pub.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'P':
                    for contract in abonnement.contract_set.all():
                        if timezone.now().date() >= contract.date_debut and timezone.now().date() <= contract.date_fin:
                            videos = videos | queryset.filter(
                                date_creation__range=(debut[0], date_fin))

            for pub in videos:
                h = Pub.objects.filter(
                    accroche=pub.accroche, panneau=pub.panneau)
                h = h.order_by("jour__date")
                z = h[0]

                for x in h:
                    if x.jour.date > z.jour.date:
                        z = x

                tarif = ""

                marque = '/'
                produit = '/'
                segment = '/'
                marche = '/'
                famille = '/'
                secteur = '/'

                if(pub.marque):
                    marque = pub.marque.Nom

                if(pub.produit):
                    produit = pub.produit.Nom

                if(pub.segment):
                    segment = pub.segment.Nom

                if(pub.marche):
                    marche = pub.marche.Nom

                if(pub.famille):
                    famille = pub.famille.Nom

                if(pub.secteur):
                    secteur = pub.secteur.Nom

                nbj = (z.jour.date - pub.jour.date)/60/60/24
                response.append({
                    "id": i,
                    'media': 'AF',
                    'date': pub.date_creation,
                    'support': '/',
                    "debut": '/',
                    "duree": '/',
                    "couleur": '/',
                    "code": pub.code,
                    "message": pub.accroche,
                    "annonceur": pub.annonceur.Nom,
                    "marque": marque,
                    "produit": produit,
                    "segment": segment,
                    "marche": marche,
                    "famille": famille,
                    "secteur": secteur,
                    "avant": '/',
                    'apres': '/',
                    "ecran": '/',
                    "afficheur": pub.panneau.afficheur.nom_afficheur,
                    "panneau": pub.panneau.type+" "+pub.panneau.mecanisme,
                    "adresse": pub.panneau.adresse,
                    "wilaya": pub.panneau.apc.commune.Wilaya.nom_wilaya,
                    "apc": pub.panneau.apc.nom_APC,
                    "typeachat": "achat classic",
                    "periodicite": "quotidienne",
                    "mois": pub.date_creation.month,
                    "datedebut": pub.jour.date,
                    "datefin": z.date_creation,
                    "nbjour": nbj,
                    "langue": pub.langue,

                    "code": pub.code,
                    'tarifbrut': pub.prix,
                    'tarifsec': '/',
                })
                i += 1
            response = sorted(response, key=lambda d: d['date'])

            # "# Article
            qs = Article.objects.none()

            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == "J":
                    for contract in abonnement.contract_set.all():
                        for annonceur in contract.annonceurs.all():
                            if contract.marques.filter(NomAnnonceur=annonceur).exists():
                                for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                    if contract.produits.filter(NomMarque=marque).exists():
                                        for produit in contract.produits.filter(NomMarque=marque):
                                            qs = qs | produit.article_set.all()
                                        qs = qs | marque.article_set.filter(
                                            produit=None)
                                    else:
                                        qs = qs | marque.article_set.all()
                                qs = qs | annonceur.article_set.filter(
                                    marque=None)

                            else:
                                qs = qs | annonceur.article_set.all()

            queryset = qs.filter(
                confirmed=True
            )
            videos = Article.objects.none()
            for abonnement in self.request.user.abonnement_set.all():
                if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'J':
                    for contract in abonnement.contract_set.all():
                        if timezone.now().date() >= contract.date_debut and timezone.now().date() <= contract.date_fin:
                            videos = videos | queryset.filter(
                                edition__date__range=(debut[0], date_fin))

            for pub in videos:

                tarif = ""

                marque = '-'
                produit = '-'
                segment = '-'
                marche = '-'
                famille = '-'
                secteur = '-'

                if(pub.marque):
                    marque = pub.marque.Nom

                if(pub.produit):
                    produit = pub.produit.Nom

                if(pub.segment):
                    segment = pub.segment.Nom

                if(pub.marche):
                    marche = pub.marche.Nom

                if(pub.famille):
                    famille = pub.famille.Nom

                if(pub.secteur):
                    secteur = pub.secteur.Nom

                response.append({
                    "id": i,
                    'media': 'Journal',
                    'date': pub.edition.date,
                    'support': pub.edition.journal.nomJournal,
                    "debut": "-",
                    "duree": "-",
                    "couleur": pub.couleur,
                    "message": pub.accroche,
                    "annonceur": pub.annonceur.Nom,
                    "marque": marque,
                    "produit": produit,
                    "segment": segment,
                    "marche": marche,
                    "famille": famille,
                    "secteur": secteur,
                    "avant": pub.page_precedente,
                    'apres': pub.page_suivante,
                    "ecran": "/",
                    "afficheur": "/",
                    "panneau":  "/",
                    "adresse":  "/",
                    "wilaya":  "/",
                    "apc":  "/",
                    "typeachat": "achat classic",
                    "periodicite": "quotidienne",
                    "mois": "",
                    "datedebut": "",
                    "datefin": "",
                    "nbjour": "",
                    "langue": "",
                    "code": pub.code,
                    'tarifbrut': '/',
                    'tarifsec': '/'
                })
                i += 1

            return Response(sorted(response, key=lambda d: d['media']))


class PigeFinaleAdminSizeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        debut = request.query_params.get('debut'),
        date_fin = request.query_params.get('date_fin')
        full = request.query_params.get('full')

        qs = Publicite.objects.all()
        queryset = qs.filter(
            confirmed=True
        )
        videos = Publicite.objects.none()

        jours = Jour.objects.filter(date__range=(
            debut[0], date_fin))
        videos = videos | queryset.filter(jour__in=jours)

        response = int(len(videos))
        return Response(response)


class PigeFinaleAdminArticleView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        debut = request.query_params.get('debut'),
        date_fin = request.query_params.get('date_fin')
        full = request.query_params.get('full')

        qs = Publicite.objects.all()
        queryset = qs.filter(
            confirmed=True
        )
        videos = Publicite.objects.none()

        jours = Jour.objects.filter(date__range=(
            debut[0], date_fin))
        videos = videos | queryset.filter(jour__in=jours)

        size = int(full) * 1000
        st = 0
        if size-1000 < 0:
            st = 0
        else:
            st = size-1000
        if size >= len(videos):
            size = len(videos)
        videos = videos[st:size]

        response = []
        i = 0
        for pub in videos:
            tarifs = TarifChaine.objects.filter(chaine=pub.jour.chaine)
            indices = Indice.objects.filter(
                chaine=pub.jour.chaine).order_by("-indice")

            tarif = tarifs.filter(debut__lte=pub.debut, fin__gte=pub.debut)

            duree = datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) if datetime.combine(date.today(), pub.fin) - datetime.combine(
                date.today(), pub.debut) >= timedelta(seconds=1) else datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) + timedelta(hours=24)
            indice = indices.filter(duree__lte=duree.total_seconds())
            ind = 1

            if len(indice) > 0:
                ind = indice[len(indice)-1].indice/100

            if(len(tarif) < 1):
                tarif = ""

            programmeAvant = Programme.objects.filter(
                jour=pub.jour, fin__lte=pub.debut)
            programmeApres = Programme.objects.filter(
                jour=pub.jour, debut__gte=pub.fin)

            if(len(programmeAvant) < 1):
                programmeAvant = Publicite.objects.filter(
                    jour=pub.jour, fin__lte=pub.debut)
            if(len(programmeApres) < 1):
                programmeApres = Publicite.objects.filter(
                    jour=pub.jour, debut__gte=pub.fin)

            marque = '/'
            produit = '/'
            segment = '/'
            marche = '/'
            famille = '/'
            secteur = '/'

            if(pub.marque):
                marque = pub.marque.Nom

            if(pub.produit):
                produit = pub.produit.Nom

            if(pub.segment):
                segment = pub.segment.Nom

            if(pub.marche):
                marche = pub.marche.Nom

            if(pub.famille):
                famille = pub.famille.Nom

            if(pub.secteur):
                secteur = pub.secteur.Nom

            response.append({
                "id": i,
                'media': 'TV',
                'date': pub.jour.date,
                'support': pub.jour.chaine.nom,
                "debut": pub.debut,
                "duree": duree,
                "couleur": '/',
                "code": pub.code,
                "message": pub.message,
                "annonceur": pub.annonceur.Nom,
                "marque": marque,
                "produit": produit,
                "segment": segment,
                "marche": marche,
                "famille": famille,
                "secteur": secteur,
                "avant": programmeAvant[0].message if len(programmeAvant) > 0 else '/',
                'apres': programmeApres[len(programmeApres)-1].message if len(programmeApres) > 0 else '/',
                "ecran": pub.ecran,
                "afficheur": "/",
                "panneau": "/",
                "adresse": "/",
                "wilaya": "/",
                "apc": "/",
                "typeachat": "achat classic",
                "periodicite": "quotidienne",
                "mois": "",
                "datedebut": "",
                "datefin": "",
                "nbjour": "",
                "langue": "",
                'tarifbrut': (((datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut))*(tarif[0].prix*ind))/30) if tarif != '' else '/',
                'tarifsec': tarif[0].prix if tarif != ''else '/'
            })
            i += 1
        response = sorted(response, key=lambda d: d['date'])
        response = sorted(response, key=lambda d: d['support'])

        qs = PubliciteRadio.objects.all()

        queryset = qs.filter(
            confirmed=True
        )
        videos = Publicite.objects.none()

        jours = JourRadio.objects.filter(date__range=(
            debut[0], date_fin))
        videos = videos | queryset.filter(jour__in=jours)

        for pub in videos:
            tarifs = TarifRadio.objects.filter(radio=pub.jour.radio)

            tarif = tarifs.filter(debut__lte=pub.debut, fin__gte=pub.debut)

            if(len(tarif) < 1):
                tarif = ""

            programmeAvant = ProgrammeRadio.objects.filter(
                jour=pub.jour, fin__lte=pub.debut)
            programmeApres = ProgrammeRadio.objects.filter(
                jour=pub.jour, debut__gte=pub.fin)

            if(len(programmeAvant) < 1):
                programmeAvant = PubliciteRadio.objects.filter(
                    jour=pub.jour, fin__lte=pub.debut)
            if(len(programmeApres) < 1):
                programmeApres = PubliciteRadio.objects.filter(
                    jour=pub.jour, debut__gte=pub.fin)

            marque = '/'
            produit = '/'
            segment = '/'
            marche = '/'
            famille = '/'
            secteur = '/'

            if(pub.marque):
                marque = pub.marque.Nom

            if(pub.produit):
                produit = pub.produit.Nom

            if(pub.segment):
                segment = pub.segment.Nom

            if(pub.marche):
                marche = pub.marche.Nom

            if(pub.famille):
                famille = pub.famille.Nom

            if(pub.secteur):
                secteur = pub.secteur.Nom

            response.append({
                "id": i,
                'media': 'RD',
                'date': pub.jour.date,
                'support': pub.jour.radio.nom,
                "debut": pub.debut,
                "duree": datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) if datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) >= timedelta(seconds=1) else datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) + timedelta(hours=24),
                "couleur": '/',
                "code": pub.code,
                "message": pub.message,
                "annonceur": pub.annonceur.Nom,
                "marque": marque,
                "produit": produit,
                "segment": segment,
                "marche": marche,
                "famille": famille,
                "secteur": secteur,
                "avant": programmeAvant[0].message if len(programmeAvant) > 0 else '/',
                'apres': programmeApres[len(programmeApres)-1].message if len(programmeApres) > 0 else '/',
                "ecran": pub.ecran,
                "afficheur": '/',
                "panneau": '/',
                "adresse": '/',
                "wilaya": '/',
                "apc": '/',
                "typeachat": "achat classic",
                "periodicite": "quotidienne",
                "mois": "",
                "datedebut": "",
                "datefin": "",
                "nbjour": "",
                "langue": "",
                'tarifbrut': ((datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut))*tarif[0].prix/30) if tarif != '' else '/',
                'tarifsec': tarif[0].prix if tarif != ''else '/'
            })
            i += 1
        response = sorted(response, key=lambda d: d['date'])

        return Response(sorted(response, key=lambda d: d['media']))


class PigeFinaleAdminView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        debut = request.query_params.get('debut'),
        date_fin = request.query_params.get('date_fin')

        # qs = Publicite.objects.all()
        # queryset = qs.filter(
        #     confirmed=True
        # )
        # videos = Publicite.objects.none()

        # jours = Jour.objects.filter(date__range=(
        #     debut[0], date_fin))
        # videos = videos | queryset.filter(jour__in=jours)

        response = []
        i = 0
        # for pub in videos:
        #     tarifs = TarifChaine.objects.filter(chaine=pub.jour.chaine)
        #     indices = Indice.objects.filter(
        #         chaine=pub.jour.chaine).order_by("-indice")

        #     tarif = tarifs.filter(debut__lte=pub.debut, fin__gte=pub.debut)

        #     duree = datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) if datetime.combine(date.today(), pub.fin) - datetime.combine(
        #         date.today(), pub.debut) >= timedelta(seconds=1) else datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) + timedelta(hours=24)
        #     indice = indices.filter(duree__lte=duree.total_seconds())
        #     ind = 1

        #     if len(indice) > 0:
        #         ind = indice[len(indice)-1].indice/100

        #     if(len(tarif) < 1):
        #         tarif = ""

        #     programmeAvant = Programme.objects.filter(
        #         jour=pub.jour, fin__lte=pub.debut)
        #     programmeApres = Programme.objects.filter(
        #         jour=pub.jour, debut__gte=pub.fin)

        #     if(len(programmeAvant) < 1):
        #         programmeAvant = Publicite.objects.filter(
        #             jour=pub.jour, fin__lte=pub.debut)
        #     if(len(programmeApres) < 1):
        #         programmeApres = Publicite.objects.filter(
        #             jour=pub.jour, debut__gte=pub.fin)

        #     marque = '/'
        #     produit = '/'
        #     segment = '/'
        #     marche = '/'
        #     famille = '/'
        #     secteur = '/'

        #     if(pub.marque):
        #         marque = pub.marque.Nom

        #     if(pub.produit):
        #         produit = pub.produit.Nom

        #     if(pub.segment):
        #         segment = pub.segment.Nom

        #     if(pub.marche):
        #         marche = pub.marche.Nom

        #     if(pub.famille):
        #         famille = pub.famille.Nom

        #     if(pub.secteur):
        #         secteur = pub.secteur.Nom

        #     response.append({
        #         "id": i,
        #         'media': 'TV',
        #         'date': pub.jour.date,
        #         'support': pub.jour.chaine.nom,
        #         "debut": pub.debut,
        #         "duree": duree,
        #         "couleur": '/',
        #         "code": pub.code,
        #         "message": pub.message,
        #         "annonceur": pub.annonceur.Nom,
        #         "marque": marque,
        #         "produit": produit,
        #         "segment": segment,
        #         "marche": marche,
        #         "famille": famille,
        #         "secteur": secteur,
        #         "avant": programmeAvant[0].message if len(programmeAvant) > 0 else '/',
        #         'apres': programmeApres[len(programmeApres)-1].message if len(programmeApres) > 0 else '/',
        #         "ecran": pub.ecran,
        #         "afficheur": "/",
        #         "panneau": "/",
        #         "adresse": "/",
        #         "wilaya": "/",
        #         "apc": "/",
        #         "typeachat": "achat classic",
        #         "periodicite": "quotidienne",
        #         "mois": "",
        #         "datedebut": "",
        #         "datefin": "",
        #         "nbjour": "",
        #         "langue": "",
        #         'tarifbrut': (((datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut))*(tarif[0].prix*ind))/30) if tarif != '' else '/',
        #         'tarifsec': tarif[0].prix if tarif != ''else '/'
        #     })
        #     i += 1
        # response = sorted(response, key=lambda d: d['date'])
        # response = sorted(response, key=lambda d: d['support'])

        # Radio
        # qs = PubliciteRadio.objects.all()

        # queryset = qs.filter(
        #     confirmed=True
        # )
        # videos = Publicite.objects.none()

        # jours = JourRadio.objects.filter(date__range=(
        #     debut[0], date_fin))
        # videos = videos | queryset.filter(jour__in=jours)

        # for pub in videos:
        #     tarifs = TarifRadio.objects.filter(radio=pub.jour.radio)

        #     tarif = tarifs.filter(debut__lte=pub.debut, fin__gte=pub.debut)

        #     if(len(tarif) < 1):
        #         tarif = ""

        #     programmeAvant = ProgrammeRadio.objects.filter(
        #         jour=pub.jour, fin__lte=pub.debut)
        #     programmeApres = ProgrammeRadio.objects.filter(
        #         jour=pub.jour, debut__gte=pub.fin)

        #     if(len(programmeAvant) < 1):
        #         programmeAvant = PubliciteRadio.objects.filter(
        #             jour=pub.jour, fin__lte=pub.debut)
        #     if(len(programmeApres) < 1):
        #         programmeApres = PubliciteRadio.objects.filter(
        #             jour=pub.jour, debut__gte=pub.fin)

        #     marque = '/'
        #     produit = '/'
        #     segment = '/'
        #     marche = '/'
        #     famille = '/'
        #     secteur = '/'

        #     if(pub.marque):
        #         marque = pub.marque.Nom

        #     if(pub.produit):
        #         produit = pub.produit.Nom

        #     if(pub.segment):
        #         segment = pub.segment.Nom

        #     if(pub.marche):
        #         marche = pub.marche.Nom

        #     if(pub.famille):
        #         famille = pub.famille.Nom

        #     if(pub.secteur):
        #         secteur = pub.secteur.Nom

        #     response.append({
        #         "id": i,
        #         'media': 'RD',
        #         'date': pub.jour.date,
        #         'support': pub.jour.radio.nom,
        #         "debut": pub.debut,
        #         "duree": datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) if datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) >= timedelta(seconds=1) else datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) + timedelta(hours=24),
        #         "couleur": '/',
        #         "code": pub.code,
        #         "message": pub.message,
        #         "annonceur": pub.annonceur.Nom,
        #         "marque": marque,
        #         "produit": produit,
        #         "segment": segment,
        #         "marche": marche,
        #         "famille": famille,
        #         "secteur": secteur,
        #         "avant": programmeAvant[0].message if len(programmeAvant) > 0 else '/',
        #         'apres': programmeApres[len(programmeApres)-1].message if len(programmeApres) > 0 else '/',
        #         "ecran": pub.ecran,
        #         "afficheur": '/',
        #         "panneau": '/',
        #         "adresse": '/',
        #         "wilaya": '/',
        #         "apc": '/',
        #         "typeachat": "achat classic",
        #         "periodicite": "quotidienne",
        #         "mois": "",
        #         "datedebut": "",
        #         "datefin": "",
        #         "nbjour": "",
        #         "langue": "",
        #         'tarifbrut': ((datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut))*tarif[0].prix/30) if tarif != '' else '/',
        #         'tarifsec': tarif[0].prix if tarif != ''else '/'
        #     })
        #     i += 1
        # response = sorted(response, key=lambda d: d['date'])

        # "# Afficheur
        qs = Pub.objects.all()
        queryset = qs.filter(
            confirmed=True
        )
        videos = Pub.objects.none()

        videos = videos | queryset.filter(
            date_creation__range=(debut[0], date_fin))

        for pub in videos:

            h = Pub.objects.filter(
                accroche=pub.accroche, panneau=pub.panneau)
            h = h.order_by("jour__date")
            z = h[0]

            for x in h:
                if x.jour.date > z.jour.date:
                    z = x

            tarif = ""

            marque = '/'
            produit = '/'
            segment = '/'
            marche = '/'
            famille = '/'
            secteur = '/'

            if(pub.marque):
                marque = pub.marque.Nom

            if(pub.produit):
                produit = pub.produit.Nom

            if(pub.segment):
                segment = pub.segment.Nom

            if(pub.marche):
                marche = pub.marche.Nom

            if(pub.famille):
                famille = pub.famille.Nom

            if(pub.secteur):
                secteur = pub.secteur.Nom

            nbj = (z.jour.date - pub.jour.date)/60/60/24

            response.append({
                "id": i,
                'media': 'AF',
                'date': pub.date_creation,
                'support': '/',
                "debut": '/',
                "duree": '/',
                "couleur": '/',
                "code": pub.code,
                "message": pub.accroche,
                "annonceur": pub.annonceur.Nom,
                "marque": marque,
                "produit": produit,
                "segment": segment,
                "marche": marche,
                "famille": famille,
                "secteur": secteur,
                "avant": '/',
                'apres': '/',
                "ecran": '/',
                "afficheur": pub.panneau.afficheur.nom_afficheur,
                "panneau": pub.panneau.type+" "+pub.panneau.mecanisme,
                "adresse": pub.panneau.adresse,
                "wilaya": pub.panneau.apc.commune.Wilaya.nom_wilaya,
                "apc": pub.panneau.apc.nom_APC,

                "typeachat": "achat classic",
                "periodicite": "quotidienne",
                "mois": pub.date_creation.month,
                "datedebut": pub.date_creation,
                "datefin": z.date_creation,
                "nbjour": nbj,
                "langue": pub.langue,


                'tarifbrut': pub.prix,
                'tarifsec': '/',

            })
            i += 1

        # "# Article

        qs = Article.objects.all()
        queryset = qs.filter(
            confirmed=True
        )
        videos = Article.objects.none()
        videos = videos | queryset.filter(edition__date__range=(
            debut[0], date_fin))

        for pub in videos:

            tarif = ""

            marque = '-'
            produit = '-'
            segment = '-'
            marche = '-'
            famille = '-'
            secteur = '-'

            if(pub.marque):
                marque = pub.marque.Nom

            if(pub.produit):
                produit = pub.produit.Nom

            if(pub.segment):
                segment = pub.segment.Nom

            if(pub.marche):
                marche = pub.marche.Nom

            if(pub.famille):
                famille = pub.famille.Nom

            if(pub.secteur):
                secteur = pub.secteur.Nom

            response.append({
                "id": i,
                'media': 'Journal',
                'date': pub.edition.date,
                'support': pub.edition.journal.nomJournal,
                "debut": "-",
                "duree": "-",
                "couleur": pub.couleur,
                "code": "12",
                "message": pub.accroche,
                "annonceur": pub.annonceur.Nom,
                "marque": marque,
                "produit": produit,
                "segment": segment,
                "marche": marche,
                "famille": famille,
                "secteur": secteur,
                "avant": pub.page_precedente,
                'apres': pub.page_suivante,
                "ecran": "/",
                "afficheur": "/",
                "panneau":  "/",
                "adresse":  "/",
                "wilaya":  "/",
                "apc":  "/",
                "typeachat": "achat classic",
                "periodicite": "quotidienne",
                "mois": "",
                "datedebut": "",
                "datefin": "",
                "nbjour": "",
                "langue": "",
                "code": pub.code,
                'tarifbrut': '/',
                'tarifsec': '/'
            })
            i += 1
        response = sorted(response, key=lambda d: d['date'])

        return Response(sorted(response, key=lambda d: d['media']))


class RechercheGenerale(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        accroche = request.query_params.get('accroche'),
        secteurReq = request.query_params.get('secteur'),

        response = []
        excel = []
        index = 0

        queryset = []

        qs = Article.objects.none()

        for abonnement in self.request.user.abonnement_set.all():
            if timezone.now().date() <= abonnement.date_fin and abonnement.service == "J":
                for contract in abonnement.contract_set.all():
                    for annonceur in contract.annonceurs.all():
                        if contract.marques.filter(NomAnnonceur=annonceur).exists():
                            for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                if contract.produits.filter(NomMarque=marque).exists():
                                    for produit in contract.produits.filter(NomMarque=marque):
                                        qs = qs | produit.article_set.all()
                                    qs = qs | marque.article_set.filter(
                                        produit=None)
                                else:
                                    qs = qs | marque.article_set.all()
                            qs = qs | annonceur.article_set.filter(
                                marque=None)

                        else:
                            qs = qs | annonceur.article_set.all()

        queryset = qs.filter(
            confirmed=True
        )
        items = Article.objects.none()
        for abonnement in self.request.user.abonnement_set.all():
            if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'J':
                for contract in abonnement.contract_set.all():
                    if timezone.now().date() >= contract.date_debut and timezone.now().date() <= contract.date_fin:
                        items = items | queryset.filter(
                            edition__date__range=(contract.date_debut, contract.date_fin))

        if secteurReq[0]:
            secteurReq = Secteur.objects.filter(id=int(secteurReq[0]))
        else:
            secteurReq = 0

        if secteurReq != 0:
            queryset = items.filter(secteur=secteurReq[0])
            queryset = queryset.filter(accroche__icontains=accroche[0])
        else:
            queryset = items.filter(accroche__icontains=accroche[0])

        for item in queryset:
            secteur = ""
            if(item.secteur):
                secteur = item.secteur.Nom
            response.append({
                "id": item.id,
                "date": item.edition.date,
                "type": "journal",
                "secteur": secteur,
                "support": item.edition.journal.nomJournal,
                "accroche": item.accroche[:25]
            })
        response = sorted(response, key=lambda d: d['date'])

        for pub in queryset:

            tarif = ""

            marque = '-'
            produit = '-'
            segment = '-'
            marche = '-'
            famille = '-'
            secteur = '-'

            if(pub.marque):
                marque = pub.marque.Nom

            if(pub.produit):
                produit = pub.produit.Nom

            if(pub.segment):
                segment = pub.segment.Nom

            if(pub.marche):
                marche = pub.marche.Nom

            if(pub.famille):
                famille = pub.famille.Nom

            if(pub.secteur):
                secteur = pub.secteur.Nom

            excel.append({
                "id": index,
                'media': 'Journal',
                'date': pub.edition.date,
                'support': pub.edition.journal.nomJournal,
                "debut": "-",
                "duree": "-",
                "couleur": pub.couleur,
                "code": "12",
                "message": pub.accroche,
                "annonceur": pub.annonceur.Nom,
                "marque": marque,
                "produit": produit,
                "segment": segment,
                "marche": marche,
                "famille": famille,
                "secteur": secteur,
                "avant": pub.page_precedente,
                'apres': pub.page_suivante,
                "ecran": "/",
                "afficheur": "/",
                "panneau":  "/",
                "adresse":  "/",
                "wilaya":  "/",
                "apc":  "/",
                "typeachat": "achat classic",
                "periodicite": "quotidienne",
                "mois": "",
                "datedebut": "",
                "datefin": "",
                "nbjour": "",
                "langue": "",
                "code": pub.code,
                'tarifbrut': '/',
                'tarifsec': '/'
            })
            index += 1
        excel = sorted(excel, key=lambda d: d['date'])

        ###########################################################################################

        qs = Publicite.objects.none()

        for abonnement in self.request.user.abonnement_set.all():
            if timezone.now().date() <= abonnement.date_fin and abonnement.service == "J":
                for contract in abonnement.contract_set.all():
                    for annonceur in contract.annonceurs.all():
                        if contract.marques.filter(NomAnnonceur=annonceur).exists():
                            for marque in contract.marques.filter(NomAnnonceur=annonceur):
                                if contract.produits.filter(NomMarque=marque).exists():
                                    for produit in contract.produits.filter(NomMarque=marque):
                                        qs = qs | produit.publicite_set.all()
                                    qs = qs | marque.publicite_set.filter(
                                        produit=None)
                                else:
                                    qs = qs | marque.publicite_set.all()
                            qs = qs | annonceur.publicite_set.filter(
                                marque=None)

                        else:
                            qs = qs | annonceur.publicite_set.all()

        queryset = qs.filter(
            confirmed=True
        )
        items = Publicite.objects.none()
        for abonnement in self.request.user.abonnement_set.all():
            if timezone.now().date() <= abonnement.date_fin and abonnement.service == 'C':
                for contract in abonnement.contract_set.all():
                    if timezone.now().date() >= contract.date_debut and timezone.now().date() <= contract.date_fin:
                        items = items | queryset.filter(
                            jour__date__range=(contract.date_debut, contract.date_fin))

        if secteurReq != 0:
            queryset = items.filter(secteur=secteurReq[0])
            queryset = queryset.filter(message__icontains=accroche[0])
        else:
            queryset = items.filter(message__icontains=accroche[0])

        for item in queryset:
            secteur = ""
            if(item.secteur):
                secteur = item.secteur.Nom
            response.append({
                "id": item.id,
                "date": item.jour.date,
                "type": "TV",
                "secteur": secteur,
                "support": item.jour.chaine.nom,
                "accroche": item.message[:25],
            })
        response = sorted(response, key=lambda d: d['date'])

        for pub in queryset:
            tarifs = TarifChaine.objects.filter(chaine=pub.jour.chaine)
            indices = Indice.objects.filter(
                chaine=pub.jour.chaine).order_by("-indice")

            tarif = tarifs.filter(debut__lte=pub.debut, fin__gte=pub.debut)

            duree = datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) if datetime.combine(date.today(), pub.fin) - datetime.combine(
                date.today(), pub.debut) >= timedelta(seconds=1) else datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut) + timedelta(hours=24)
            indice = indices.filter(duree__lte=duree.total_seconds())
            ind = 1

            if len(indice) > 0:
                ind = indice[len(indice)-1].indice/100

            if(len(tarif) < 1):
                tarif = ""

            programmeAvant = Programme.objects.filter(
                jour=pub.jour, fin__lte=pub.debut)
            programmeApres = Programme.objects.filter(
                jour=pub.jour, debut__gte=pub.fin)

            if(len(programmeAvant) < 1):
                programmeAvant = Publicite.objects.filter(
                    jour=pub.jour, fin__lte=pub.debut)
            if(len(programmeApres) < 1):
                programmeApres = Publicite.objects.filter(
                    jour=pub.jour, debut__gte=pub.fin)

            marque = '/'
            produit = '/'
            segment = '/'
            marche = '/'
            famille = '/'
            secteur = '/'

            if(pub.marque):
                marque = pub.marque.Nom

            if(pub.produit):
                produit = pub.produit.Nom

            if(pub.segment):
                segment = pub.segment.Nom

            if(pub.marche):
                marche = pub.marche.Nom

            if(pub.famille):
                famille = pub.famille.Nom

            if(pub.secteur):
                secteur = pub.secteur.Nom

            excel.append({
                "id": index,
                'media': 'TV',
                'date': pub.jour.date,
                'support': pub.jour.chaine.nom,
                "debut": pub.debut,
                "duree": duree,
                "couleur": '/',
                "code": pub.code,
                "message": pub.message,
                "annonceur": pub.annonceur.Nom,
                "marque": marque,
                "produit": produit,
                "segment": segment,
                "marche": marche,
                "famille": famille,
                "secteur": secteur,
                "avant": programmeAvant[0].message if len(programmeAvant) > 0 else '/',
                'apres': programmeApres[len(programmeApres)-1].message if len(programmeApres) > 0 else '/',
                "ecran": pub.ecran,
                "afficheur": "/",
                "panneau": "/",
                "adresse": "/",
                "wilaya": "/",
                "apc": "/",
                "typeachat": "achat classic",
                "periodicite": "quotidienne",
                "mois": "",
                "datedebut": "",
                "datefin": "",
                "nbjour": "",
                "langue": "",
                'tarifbrut': (((datetime.combine(date.today(), pub.fin) - datetime.combine(date.today(), pub.debut))*(tarif[0].prix*ind))/30) if tarif != '' else '/',
                'tarifsec': tarif[0].prix if tarif != ''else '/'
            })
            index += 1
        excel = sorted(excel, key=lambda d: d['date'])
        excel = sorted(excel, key=lambda d: d['support'])

        excel = sorted(excel, key=lambda d: d['media'])
        response = sorted(response, key=lambda d: d['secteur'])

        response = {
            "excel": excel,
            "response": response
        }

        return Response(response)
