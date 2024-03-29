from django.urls import path

from django.conf.urls import include
from rest_framework import routers
from .views import *

urlpatterns = [
    path('journaux/<int:pk>', UpdateJournalView.as_view()),


    path('journaux', JournalView.as_view()),


    path('journaux/search/', Journalsearch.as_view()),
    path('journaux/test/', JournalViewTest.as_view()),

    path('journaux/client/', JournalClientView.as_view()),



    path('editions/search', EditionSearch.as_view()),
    path('editions/client/', EditionSearchClient.as_view()),
    path('editions/', EditionView.as_view()),
    path('editions/<int:pk>/', UpdateEditioneView.as_view()),
    path('editions/count/', Editioncount.as_view()),

    path('articles', ArticleView.as_view()),
    path('articles/post/', PostArticleView.as_view()),
    path('articles/confirmed/', ArticleConfirmed.as_view()),
    path('articles/confirmed/count/', ArticleConfirmedCount.as_view()),
    path('articles/<int:pk>/', UpdateArticleView.as_view()),
    path('articles/filter', SearchFilter.as_view()),
    path('articles/search/', Articlesearch.as_view()),
    path('articles/info/', getProduitMarqueAnnonceur.as_view()),
    path('articles/client/', getProduitMarqueAnnonceur.as_view()),


    path('jourafficheur/', JourAfficheurView.as_view()),
    path('jourafficheur/<int:pk>/', JourAfficheurDetail.as_view()),

    path('afficheur/', getAfficheurInfo.as_view()),
    path('afficheur/post/', AfficheurView.as_view()),
    path('afficheur/post/<int:pk>/', AfficheurDetail.as_view()),
    path('afficheur/search/', Afficheursearch.as_view()),


    path('panneau/', PanneauView.as_view()),
    path('panneau/<int:pk>/', PanneauDetail.as_view()),
    path('panneau/filter/', PanneauFilter.as_view()),

    path('pubFalse/', PubViewFalse.as_view()),
    path('pubTrue/', PubViewTrue.as_view()),
    path('pubAjout/', PubViewTest.as_view()),
    path('pub/count/', PubCount.as_view()),
    path('pub/codes/', PubCodes.as_view()),
    path('pub/<int:pk>/', PubDetail.as_view()),
    path('pub/filter/', PubFilter.as_view()),
    path('pub/confirmed/', PubConfirmation.as_view()),
    path('pub/confirmed/count/', PubConfirmedCount.as_view()),

    path('annonceur/', AnnonceurView.as_view()),
    path('annonceur/exists/', AnnonceurExiste.as_view()),
    path('getannonceurs/', GetAnnonceurs.as_view()),
    path('annonceur/<int:pk>/', AnnonceurDetail.as_view()),
    path('annonceur/search/', Annonceursearch.as_view()),

    path('segment/', SegmentView.as_view()),
    path('segment/<int:pk>/', SegmentDetail.as_view()),
    path('getsegments/', GetSegmentsView.as_view()),


    path('marche/', MarcheView.as_view()),
    path('marche/<int:pk>/', MarcheDetail.as_view()),
    path('getmarches/', GetMarchesView.as_view()),


    path('famille/', FamilleView.as_view()),
    path('famille/<int:pk>/', FamilleDetail.as_view()),
    path('getfamilles/', GetFamillesView.as_view()),


    path('secteur/', SecteurView.as_view()),
    path('secteur/<int:pk>/', SecteurDetail.as_view()),
    path('getsecteurs/', GetSecteursView.as_view()),




    path('marque/', MarqueView.as_view()),
    path('getmarques/', GetMarques.as_view()),
    path('marque/<int:pk>/', MarqueDetail.as_view()),
    path('marque/info/', MarqueInfo.as_view()),
    path('marque/exists/', MarqueExiste.as_view()),
    path('marque/contract', MarqueSearchContract.as_view()),
    path('marque/filter', MarqueFilter.as_view()),
    path('marque/search/', MarqueSearch.as_view()),
    path('marque/filterforcontract', MarqueFilterForContract.as_view()),


    path('produit/', ProduitView.as_view()),
    path('getproduits/', GetProduits.as_view()),
    path('produit/exists/', ProduitExiste.as_view()),
    path('produit/<int:pk>/', ProduitDetail.as_view()),
    path('produit/filter', ProduitFilter.as_view()),
    path('produit/search/', ProduitSearch.as_view()),
    path('produit/filterforcontract', ProduitFilterForContract.as_view()),


    path('abonnement/', AbonnementView.as_view()),
    path('abonnement/<int:pk>', AbonnementDetail.as_view()),
    path('abonnement/search/', Abonnementsearch.as_view()),

    path('contract/', ContractView.as_view()),
    path('contract/post/', ContractPost.as_view()),
    path('contract/<int:pk>', ContractDetail.as_view()),
    path('contract/search/', Contractsearch.as_view()),

    path('wilaya/', WilayaView.as_view()),

    path('apc/', ApcView.as_view()),
    path('apc/search/', Apcsearch.as_view()),

    path('commune/', CommuneView.as_view()),
    path('commune/search/', Communesearch.as_view()),
    path('articleclient/', ArticleClientView.as_view()),
    path('pubclient/', PubClientView.as_view()),

    path('clientabonnement/', ClientAbonnement.as_view()),
    path('clientcontart/', ContractViewClient.as_view()),

    path('chaine/', ChaineView.as_view()),
    path('chaine/getall/', ChaineAllView.as_view()),
    path('chaine/<int:pk>/', ChaineDetail.as_view()),
    path('chaine/search/', Chainesearch.as_view()),

    path('video/recherche/', RecherchePublicite.as_view()),


    path('video/', PubliciteView.as_view()),
    path('video/post/', PostPubliciteView.as_view()),
    path('video/post/existe/', PostPubliciteExisteView.as_view()),
    path('video/messages/', GetMessagesView.as_view()),
    path('video/temp/<int:pk>/', ModifierTempView.as_view()),

    path('programme/', ProgrammeView.as_view()),
    path('programme/<int:pk>/', UpdateProgrammeView.as_view()),
    path('jour/', JourView.as_view()),
    path('jourclient/', JourViewClient.as_view()),
    path('jour/<int:pk>/', JourDetail.as_view()),
    path('tableprogramme/', ProgrammeEtPub.as_view()),
    path('tableprogrammeclient/', ChaneiClientView.as_view()),
    # path('video/search/', VideoView.as_view()),
    path('video/<int:pk>/', PubliciteDetail.as_view()),
    path('video/confirmed/', VideoConfirmation.as_view()),
    path('video/confirmed/count/', VideoConfirmedCount.as_view()),
    path('videoclient/<int:pk>/', PubliciteClientDetail.as_view()),
    # RADIO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    path('radio/', RadioView.as_view()),
    path('radio/getall/', RadioAllView.as_view()),
    path('radio/<int:pk>/', RadioDetail.as_view()),
    path('radio/search/', Radiosearch.as_view()),

    path('son/', PubliciteRadioView.as_view()),
    path('son/post/', PostPubliciteRadioView.as_view()),
    path('programmeradio/', ProgrammeRadioView.as_view()),
    path('programmeradio/<int:pk>/', UpdateProgrammeRadioView.as_view()),
    path('jourradio/', JourRadioView.as_view()),
    path('jourradioclient/', JourRadioViewClient.as_view()),
    path('jourradio/<int:pk>/', JourRadioDetail.as_view()),
    path('tableprogrammeradio/', ProgrammeEtPubRadio.as_view()),
    path('tableprogrammeradioclient/', RadioClientView.as_view()),
    # path('video/search/', VideoView.as_view()),
    path('son/<int:pk>/', PubliciteRadioDetail.as_view()),
    path('son/confirmed/', SonConfirmation.as_view()),
    path('son/confirmed/count/', SonConfirmedCount.as_view()),
    path('sonclient/<int:pk>/', PubliciteRadioClientDetail.as_view()),




    path('articles/link/', ArticleLinkClient.as_view()),
    path('pub/link/', PubLinkClient.as_view()),
    path('publicite/link/', PubliciteLinkClient.as_view()),


    path('sendemail/', send_email.as_view()),
    path('sendemailchaine/', send_email_chaine.as_view()),


    path('gettarifchaine/', GetTarifChaineView.as_view()),
    path('tarifchaine/', TarifChaineView.as_view()),
    path('tarifchaine/<int:pk>/', TarifChaineDetail.as_view()),

    path('indice/', IndiceView.as_view()),
    path('indice/<int:pk>/', IndiceDetail.as_view()),

    path('gettarifradio/', GetTarifRadioView.as_view()),
    path('tarifradio/', TarifRadioView.as_view()),
    path('tarifradio/<int:pk>/', TarifRadioDetail.as_view()),

    path('pigesfinale/', PigeFinaleView.as_view()),
    path('pigesfinalesize/', PigeFinaleSizeView.as_view()),
    path('pigesfinalepublicite/', PigeFinalePubliciteView.as_view()),



    path('pigesfinaleadmin/', PigeFinaleAdminView.as_view()),
    path('pigesfinaleadminarticle/', PigeFinaleAdminArticleView.as_view()),
    path('pigesfinaleadminsize/', PigeFinaleAdminSizeView.as_view()),



    path('recherchegenerale/', RechercheGenerale.as_view()),



]
