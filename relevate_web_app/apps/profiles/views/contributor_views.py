import json
import os
from datetime import datetime as dt

from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View

from apps.profiles.modules.list_of_universities import WORLD_UNIVERSITIES_LISTS
from ..forms.contributor_form import ContributorForm
from ..models.adviser_model import Adviser
from ..models.contributor_model import ContributorProfile, Address, PendingContributors, DeniedContributors, \
    AcademicProfile, ContributorCertification, OrganizationalAffiliation
from ..models.user_models import UserProfile
from ..modules.contributor_util import validate_academic_and_cert, update_contributor_qualification, \
    get_max_academic_id, get_max_certificate_id, get_max_affiliation_id, get_list_of_contributor_credentials, get_contributor_highest_degree
from ...contribution.models.topic_model import Topics
from ...contribution.modules.post_util import display_error
from ...contribution.modules.search_util import find_universities
from ..forms.authentication_forms import UpdateUserForm
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import os.path
from django.conf import settings
from PIL import Image

DEBUG = False
BETA = True
organization_list = ('National Council on Family Relations (NCFR)',
                     'American Association for Marriage and Family Therapy (AAMFT)',
                     'Society for the Study of Emerging Adulthood (SSEA)',
                     'International Association for Relationship Research (IARR)',
                     'American Family Therapy Academy (AFTA)',
                     'American Psychological Association (APA)',
                     'National Communication Association (NCA)',
                     'Society for Prevention Research (SPR)')

class ContributorCreateView(LoginRequiredMixin, View):
    """
    Contains LoginRequiredMixin
    """

    def get(self, request):
        """
        Creates an instance of ``ContributorForm`` and populates it with options
        for all currently advisers as well as all available topics.
        """
        user_prof = UserProfile.objects.get(user=request.user)
        if not (user_prof.is_contributor):
            tag_names = Topics.objects.all().order_by('name')
            advisers = Adviser.objects.filter(is_active=True)

            organization_list = ('National Council on Family Relations (NCFR)',
                                 'American Association for Marriage and Family Therapy (AAMFT)',
                                 'Society for the Study of Emerging Adulthood (SSEA)',
                                 'International Association for Relationship Research (IARR)',
                                 'American Family Therapy Academy (AFTA)',
                                 'American Psychological Association (APA)',
                                 'National Communication Association (NCA)',
                                 'Society for Prevention Research (SPR)')
            contribution_form = ContributorForm(data_list=organization_list)

            return render(request, 'contributor_create.html',
                          {
                              'form': contribution_form,
                              'user_prof': user_prof,
                              'tag_names': tag_names,
                              'advisers': advisers,
                              # 'institute': WORLD_UNIVERSITIES_LISTS[0:30],
                          }
                          )
        else:
            return HttpResponseRedirect(reverse_lazy('contribution:home'))

    def post(self, request):
        """
        If the form is valid, an ``Address`` object is created, then
        a ``ContributorProfile`` object is created. If the contributor
        is to have an ``Adviser``, that is created as well. All expertise
        topics the contributor has selected are attached to his/her profile.

        If the form is not valid, the errors are rendered as messages to the user,
        and the form is re-rendered.

        If the ``BETA`` variable is set to true, the contributor is automatically approved. Otherwise,
        they are placed into the ``PendingContributors`` table for staff approval.
        """
        form = ContributorForm(request.POST, request.FILES)
        user_prof = UserProfile.objects.get(user=request.user)
        academics_req = request.POST.get('academicList')
        print ("academic_req ", academics_req)
        cert_req = request.POST.get('certificateList')
        print ("cert req ", cert_req)
        affiliation_req = request.POST.get('affiliationList')
        print("affiliation_list", affiliation_req)
        is_academics_and_cert_valid = validate_academic_and_cert(academics_req, request)
        if form.is_valid() and is_academics_and_cert_valid:
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            avatar = form.cleaned_data.get('avatar')
            address = Address(
                street_address=form.cleaned_data.get('address'),
                city=form.cleaned_data.get('city'),
                state=form.cleaned_data.get('state'),
                zipcode=form.cleaned_data.get('zipcode'),
                country=form.cleaned_data.get('country')
            )
            address.save()
            contributor_profile = ContributorProfile(
                user_profile=user_prof,
                website_url=form.cleaned_data.get('website_url'),
                cv=form.cleaned_data.get('cv'),
                biography_text=form.cleaned_data.get('biography'),
                address=address,
                interests=form.cleaned_data.get('interests'),
                avatar=form.cleaned_data.get('avatar'),
                accept_terms=form.cleaned_data.get('accept_terms'),
            )
            if (form.cleaned_data.get('avatar')):
                # Gets the original image to be cropped
                photo = Image.open(form.cleaned_data.get('avatar'))
                # Cropps the image using values x,y,w,and h from the form
                cropped_image = photo.crop((x, y, w + x, h + y))
                # Splits the file name and the extension
                filename, file_extension = os.path.splitext(os.path.basename(urlparse(contributor_profile.avatar.url).path))
                cropped_image.save(settings.BASE_DIR + "/media/user_profiles/avatar/" + filename + file_extension)
                contributor_profile.avatar = "user_profiles/avatar/" + filename + file_extension
            if (form.cleaned_data.get('adviser') != None):
                contributor_profile.has_adviser = True
                contributor_profile.advisers_profile = form.cleaned_data.get('adviser')
            topics = form.cleaned_data.get('area_of_expertise')
            contributor_profile.save()
            for t in topics:
                contributor_profile.expertise_topics.add(t)
            # @US_TODO: Remove this after Beta
            if (not BETA):
                pending_contributors = PendingContributors(contributor=contributor_profile)
                pending_contributors.save()
                messages.success(request, 'Your application has been submitted and being reviewed!')
            else:
                user_prof.is_contributor = True
                contributor_profile.is_approved = True
                user_prof.save()
                contributor_profile.save()
                messages.success(request, 'BETA: You are now a contributor!')
            update_contributor_qualification(academics_req, cert_req, affiliation_req, contributor_profile,
                                             update=False)
            return HttpResponseRedirect(reverse_lazy('contribution:home'))
        else:
            display_error(form, request)
            return render(request, 'contributor_create.html',
                          {
                              'form': form,
                              'user_prof': user_prof,
                              'tag_names': Topics.objects.all().order_by('name'),
                              # 'institute': WORLD_UNIVERSITIES_LISTS[0:30], @TODO might need to use own database eventually
                          })


class ContributorUpdateView(LoginRequiredMixin, View):
    """
    Contains LoginRequiredMixin that checks for a log in status
    """

    def get(self, request):
        '''
        Gets the form for updating a contributor profile.
        '''
        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        contributor_profile = ContributorProfile.objects.get(user_profile=user_prof)
        if contributor_profile.has_adviser:
            adviser_id = contributor_profile.advisers_profile.id
        else:
            adviser_id = -1
        topics = contributor_profile.expertise_topics.all()
        already_sel = []
        for t in topics:
            already_sel.append(t)
        tag_names = Topics.objects.all()
        academic_profile = AcademicProfile.objects.filter(contributor_profile=contributor_profile)
        certifications = ContributorCertification.objects.filter(contributor_profile=contributor_profile)
        max_certification_id = get_max_certificate_id(certifications)
        organizational_affiliations = OrganizationalAffiliation.objects.filter(contributor_profile=contributor_profile)
        max_academic_id = get_max_academic_id(academic_profile)
        user_form = UpdateUserForm({
            'first_name': user.first_name,
            'last_name': user.last_name,
            "email": user.email
        })
        contribution_form = ContributorForm({
            'user_profile': user_prof,
            'address': contributor_profile.address.street_address,
            'city': contributor_profile.address.city,
            'state': contributor_profile.address.state,
            'country': contributor_profile.address.country,
            'zipcode': contributor_profile.address.zipcode,
            'website_url': contributor_profile.website_url,
            'interests': contributor_profile.interests,
            'area_of_expertise': already_sel,
            'avatar': contributor_profile.avatar,
            'adviser': adviser_id,
            'biography': contributor_profile.biography_text,
            'accept_terms': contributor_profile.accept_terms,
        }, data_list=organization_list)
        obj = {
            'form': contribution_form,
            'user_form': user_form,
            'user_prof': user_prof,
            'already_sel': already_sel,
            'contrib_prof': contributor_profile,
            'tag_names': tag_names,
            'cv_name': os.path.basename(contributor_profile.cv.name),
            'academic_profiles': academic_profile,
            'certifications': certifications,
            'max_academic_id': max_academic_id,
            'max_certification_id': max_certification_id,
            'organizational_affiliations': organizational_affiliations
        }
        if (contributor_profile.avatar):
            obj['avatar_name'] = contributor_profile.avatar.url
        return render(request, 'contributor_update.html', obj)

    def post(self, request):
        '''
        Performs the update of the contributor profile after checking the
        validity of the form.
        '''
        form = ContributorForm(request.POST, request.FILES)
        user_form = UpdateUserForm(request.POST)
        user_prof = UserProfile.objects.get(user=request.user)
        cp = ContributorProfile.objects.get(user_profile=user_prof)
        academics_req = request.POST.get('academicList')
        cert_req = request.POST.get('certificateList')
        org_req = request.POST.get('affiliationList')
        is_academics_and_cert_valid = validate_academic_and_cert(academics_req, request)
        print("here are errors!!!!!!!!!")
        print (user_form.errors)
        if user_form.is_valid() and form.is_valid() and is_academics_and_cert_valid:
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            avatar = form.cleaned_data.get('avatar')
            # Update User name, email
            user_prof.user.first_name = user_form.cleaned_data.get('first_name')
            user_prof.user.last_name = user_form.cleaned_data.get('last_name')
            user_prof.user.email = user_form.cleaned_data.get('email')
            user_prof.user.save()
            # Address Stuff
            cp.address.street_address = form.cleaned_data.get('address')
            cp.address.city = form.cleaned_data.get('city')
            cp.address.state = form.cleaned_data.get('state')
            cp.address.country = form.cleaned_data.get('country')
            cp.zipcode = form.cleaned_data.get('zipcode')
            cp.address.save()
            # Avatar
            if (form.cleaned_data.get('avatar')):
                # Gets the original image to be cropped
                photo = Image.open(form.cleaned_data.get('avatar'))
                # Cropps the image using values x,y,w,and h from the form
                cropped_image = photo.crop((x, y, w + x, h + y))
                # Splits the file name and the extension
                filename, file_extension = os.path.splitext(os.path.basename(urlparse(cp.avatar.url).path))
                cropped_image.save(settings.BASE_DIR + "/media/user_profiles/avatar/" + filename + file_extension)
                cp.avatar = "user_profiles/avatar/" + filename + file_extension

            # Interests
            cp.interests = form.cleaned_data.get('interests')
            print("%s length of bio" % str(len(form.cleaned_data.get('biography'))))
            # Bio
            cp.biography_text = form.cleaned_data.get('biography')

            # CV
            if (form.cleaned_data.get('cv')):
                cp.cv = form.cleaned_data.get('cv')

            if (form.cleaned_data.get('adviser') != None):
                cp.has_adviser = True
                cp.advisers_profile = form.cleaned_data.get('adviser')
            cp.save()

            # Website Url
            cp.website_url = form.cleaned_data.get('website_url')

            curr_topics = cp.expertise_topics.all()
            for each_topic in curr_topics:
                try:
                    cp.expertise_topics.remove(each_topic)
                except ObjectDoesNotExist:
                    pass
            for each_topic in form.cleaned_data.get('area_of_expertise'):
                cp.expertise_topics.add(each_topic)
            cp.save()
            update_contributor_qualification(academics_req, cert_req, org_req, cp)
            messages.success(request, 'Your profile has been updated!')
            return HttpResponseRedirect(reverse('profile:contributor_profile'))
        else:
            display_error(form, request)
            academic_profiles = AcademicProfile.objects.filter(contributor_profile=cp)
            certifications = ContributorCertification.objects.filter(contributor_profile=cp)
            affiliations = OrganizationalAffiliation.objects.filter(contributor_profile=cp)
            max_academic_id = get_max_academic_id(academic_profiles)  # counter for unique table id
            max_certification_id = get_max_certificate_id(certifications)  # counter for unique id
            max_affiliation_id = get_max_academic_id(affiliations)   # counter for unique id
            topics = cp.expertise_topics.all()
            already_sel = []
            if cp.has_adviser:
                adviser_id = cp.advisers_profile.id
            else:
                adviser_id = -1
            for t in topics:
                already_sel.append(t)
            form = ContributorForm({
                'user_profile': user_prof,
                'address': cp.address.street_address,
                'city': cp.address.city,
                'state': cp.address.state,
                'country': cp.address.country,
                'zipcode': cp.address.zipcode,
                'website_url': cp.website_url,
                'interests': cp.interests,
                'area_of_expertise': already_sel,
                'avatar': cp.avatar,
                'adviser': adviser_id,
                'biography': cp.biography_text,
                'accept_terms': cp.accept_terms,
            }, data_list=organization_list)
            return render(request, 'contributor_update.html',
                          {
                              'form': form,
                              'user_form': user_form,
                              'user_prof': user_prof,
                              'already_sel': cp.expertise_topics.all().order_by('-name'),
                              'contrib_prof': cp,
                              'tag_names': Topics.objects.all(),
                              'academic_profiles': academic_profiles,
                              'certifications': certifications,
                              'max_academic_id': max_academic_id,
                              'max_certification_id': max_certification_id,
                              'max_affiliation_id': max_affiliation_id
                          })


class ContributorProfileView(LoginRequiredMixin, View):
    """
    Contains LoginRequiredMixin
    """

    def get(self, request):
        '''
        Gets the contributor profile for viewing only by the actual
        contributor that owns it.
        '''
        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        if (user_prof.is_contributor):
            contributor_profile = ContributorProfile.objects.get(user_profile=user_prof)
            expertise_topics = contributor_profile.expertise_topics.all().order_by('name')
            academic_prof = AcademicProfile.objects.filter(contributor_profile=contributor_profile)
            certifications = ContributorCertification.objects.filter(contributor_profile=contributor_profile)
            organizational_affiliations = OrganizationalAffiliation.objects.filter(
                contributor_profile=contributor_profile)
            highest_ranking_degree = get_contributor_highest_degree(academic_prof)
            return render(request, "contributor_profile.html",
                          {
                              "user_prof": user_prof,
                              "contrib_prof": contributor_profile,
                              "expertise_topics": expertise_topics,
                              "academic_prof": academic_prof,
                              "certifications": certifications,
                              'highest_ranking_degree': highest_ranking_degree,
                              'organizational_affiliations': organizational_affiliations
                          })
        else:
            return HttpResponseRedirect(reverse_lazy('contribution:home'))


class PublicContributorProfileView(View):
    def get(self, request, contrib_id):
        '''
        Gets the public facing contributor profile page viewable by anyone.

        :param contrib_id: The id of the contributors page that you want to view
        '''
        user = request.user

        if (user.is_authenticated):
            user_prof = UserProfile.objects.get(user=user)
        else:
            user_prof = None

        try:
            contrib_prof = ContributorProfile.objects.get(id=contrib_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse_lazy('contribution:home'))

        expertise_topics = contrib_prof.expertise_topics.all().order_by('name')
        academic_prof = AcademicProfile.objects.filter(contributor_profile=contrib_prof)
        certifications = ContributorCertification.objects.filter(contributor_profile=contrib_prof)
        organizational_affiliations = OrganizationalAffiliation.objects.filter(contributor_profile=contrib_prof)
        highest_ranking_degree = get_contributor_highest_degree(academic_prof)
        return render(request, 'public_contributor_profile.html',
                      {
                          'user_prof': user_prof,
                          'contrib_prof': contrib_prof,
                          'expertise_topics': expertise_topics,
                          "academic_prof": academic_prof,
                          "certifications": certifications,
                          "highest_ranking_degree": highest_ranking_degree,
                          'organizational_affiliations': organizational_affiliations
                      })


# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-


class ContributorListView(View):
    def get(self, request):
        '''
        Returns a listing of all contributors that are currently
        approved.
        '''
        user = request.user
        contributor_profiles = ContributorProfile.objects.filter(is_approved=True)
        if (user.is_authenticated):
            user_prof = UserProfile.objects.get(user=request.user)
            return render(request, 'contributors.html',
                          {
                              'user_prof': user_prof,
                              'contributors': get_list_of_contributor_credentials(contributor_profiles),
                          })
        else:
            return render(request, 'contributors.html',
                          {
                              'contributors': get_list_of_contributor_credentials(contributor_profiles)
                          })


class DeniedContributorListView(LoginRequiredMixin, View):
    """
    Contains LoginRequiredMixin
    """

    def get(self, request):
        '''
        If the user is a member of the staff, send them to the page
        where the denied contributors are listed. Otherwise, send them
        home.
        '''
        if (request.user.is_staff):
            user_prof = UserProfile.objects.get(user=request.user)
            denials = DeniedContributors.objects.all()
            return render(request, "denied_contributors.html",
                          {
                              'user_prof': user_prof,
                              'contributors': denials
                          })
        else:
            return HttpResponseRedirect(reverse_lazy("contribution:home"))


class ContributorApproveView(LoginRequiredMixin, View):
    """
    Contains LoginRequiredMixin
    """

    def get(self, request):
        '''
        Checks if the user is a member of the staff, if they
        are, send them to the page to approve or deny contributor
        applications. Otherwise, send them to the home page.
        '''
        if (request.user.is_staff):
            user_prof = UserProfile.objects.get(user=request.user)
            pending_contributors = PendingContributors.objects.values_list('contributor', flat=True)
            contributor_profiles = ContributorProfile.objects.filter(id__in=pending_contributors)
            credentials = get_list_of_contributor_credentials(contributor_profiles)
            for i in range(len(contributor_profiles)):
                contributor_profiles[i].credentials = credentials[i]['credentials']
            return render(request, "contributor_approve.html",
                          {
                              'user_prof': user_prof,
                              'contributors': contributor_profiles,
                          })
        else:
            return HttpResponseRedirect(reverse("contribution:home"))


class ApproveButtonView(View):
    '''
    AJAX View
    '''

    def post(self, request):
        '''
        Actually handles the AJAX request to approve a contributor
        and remove them from the pending contributors queue
        '''
        request_id = request.POST.get("id")
        contrib_prof = ContributorProfile.objects.get(id=int(request_id))
        user_prof = contrib_prof.user_profile
        print("Approving User: " + user_prof.user.first_name + " " + user_prof.user.last_name)
        user_prof.is_contributor = True
        user_prof.save()
        contrib_prof.is_approved = True
        contrib_prof.save()
        PendingContributors.objects.filter(contributor_id=contrib_prof.id).delete()
        return HttpResponse('')


class DenyButtonView(View):
    '''
    AJAX View
    '''

    def post(self, request):
        '''
        Actually handles the AJAX request to deny a contributor
        and remove them from the pending contributors queue
        '''
        request_id = request.POST.get("id")
        reason = request.POST.get('reason')
        contrib_prof = ContributorProfile.objects.get(id=int(request_id))
        user_prof = contrib_prof.user_profile
        print("Denying User: " + user_prof.user.first_name + " " + user_prof.user.last_name)
        PendingContributors.objects.filter(contributor_id=contrib_prof.id).delete()
        denial = DeniedContributors(contributor=contrib_prof,
                                    date_denied=dt.utcnow(),
                                    reason=reason)
        denial.save()
        # @US_TODO: Send an email here upon denial
        return HttpResponse("")


class QueryUniversities(View):
    '''
    AJAX View
    '''

    def get(self, request):
        '''
        Actually handles the AJAX request for real time searching
        of the database for university names.
        '''
        response = {}
        query_word = request.GET.get('query_word')
        list_of_uni = find_universities(query_word)
        response['universities'] = list(list_of_uni)
        return HttpResponse(HttpResponse(json.dumps(response), status=201))
