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
from ..forms.contributor_form import ContributorForm, ContributorUpdateForm
from ..models.adviser_model import Adviser
from ..models.contributor_model import ContributorProfile, Address, PendingContributors, DeniedContributors, \
    AcademicProfile, ContributorCertification, OrganizationalAffiliation, ContributorProfileUnfinished, \
AddressUnfinished, AcademicProfileUnfinished, ContributorCertificationUnfinished, \
    OrganizationalAffiliationUnfinished
from ..models.user_models import UserProfile
from ..modules.contributor_util import validate_academic_and_cert, update_contributor_qualification, \
    get_max_academic_id, get_max_certificate_id, get_max_affiliation_id, get_list_of_contributor_credentials, get_contributor_highest_degree, \
    unfinished_contributor_qualification
from ...contribution.models.topic_model import Topics
from ...contribution.modules.post_util import display_error
from ...contribution.modules.search_util import find_universities
from ..forms.authentication_forms import UpdateUserForm
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import os.path
from django.conf import settings
from PIL import Image

DEBUG = False
BETA = False
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
        organization_list = ('National Council on Family Relations (NCFR)',
                             'American Association for Marriage and Family Therapy (AAMFT)',
                             'Society for the Study of Emerging Adulthood (SSEA)',
                             'International Association for Relationship Research (IARR)',
                             'American Family Therapy Academy (AFTA)',
                             'American Psychological Association (APA)',
                             'National Communication Association (NCA)',
                             'Society for Prevention Research (SPR)')
        user_prof = UserProfile.objects.get(user=request.user)
        #check for previous saved information to fill out form with
        if not (user_prof.is_contributor and not user_prof.is_pending_contributor):
            advisers = Adviser.objects.filter(is_active=True)
            previous_form = ContributorProfileUnfinished.objects.filter(user_profile_id=user_prof.id).first()
            if previous_form:
                topics = previous_form.expertise_topics.all()
                already_sel = []
                for t in topics:
                    already_sel.append(t)
                tag_names = Topics.objects.all()
                academic_profile = AcademicProfileUnfinished.objects.filter(contributor_profile=previous_form)
                for a in academic_profile:
                    print(a.program)
                certifications = ContributorCertificationUnfinished.objects.filter(contributor_profile=previous_form)
                for c in certifications:
                    print(c.name_of_certification)
                max_certification_id = get_max_certificate_id(certifications)
                organizational_affiliations = OrganizationalAffiliationUnfinished.objects.filter(
                    contributor_profile=previous_form)
                for o in organizational_affiliations:
                    print(o.name_of_affiliation)
                max_academic_id = get_max_academic_id(academic_profile)
                contribution_form = ContributorForm({
                    'user_profile': user_prof,
                    'address': previous_form.address.street_address,
                    'city': previous_form.address.city,
                    'state': previous_form.address.state,
                    'country': previous_form.address.country,
                    'zipcode': previous_form.address.zipcode,
                    'website_url': previous_form.website_url,
                    'interests': previous_form.interests,
                    'area_of_expertise': already_sel,
                    'avatar': previous_form.avatar,
                    'biography': previous_form.biography_text,
                    'accept_terms': previous_form.accept_terms
                }, data_list=organization_list)
                obj = {
                    'form': contribution_form,
                    'user_prof': user_prof,
                    'already_sel': already_sel,
                    'tag_names': tag_names,
                    'cv_name': os.path.basename(previous_form.cv.name),
                    'academic_profiles': academic_profile,
                    'certifications': certifications,
                    'max_academic_id': max_academic_id,
                    'max_certification_id': max_certification_id,
                    'organizational_affiliations': organizational_affiliations,
                    'advisers': advisers
                }
                if (previous_form.avatar):
                    obj['avatar_name'] = previous_form.avatar.url
                return render(request, 'contributor_create.html', obj)
            tag_names = Topics.objects.all().order_by('name')
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
        form = ContributorForm(request.POST, request.FILES, data_list=organization_list)
        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        academics_req = request.POST.get('hiddenAcaTable')
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
                # # Gets the original image to be cropped
                # photo = Image.open(form.cleaned_data.get('avatar'))
                # # Cropps the image using values x,y,w,and h from the form
                # cropped_image = photo.crop((x, y, w + x, h + y))
                # # Splits the file name and the extension
                # filename, file_extension = os.path.splitext(os.path.basename(urlparse(contributor_profile.avatar.url).path))
                # cropped_image.save(settings.BASE_DIR + "/media/user_profiles/avatar/" + filename + file_extension)
                # contributor_profile.avatar = "user_profiles/avatar/" + filename + file_extension
                contributor_profile.avatar = form.cleaned_data.get('avatar')
            if (form.cleaned_data.get('adviser') != None):
                contributor_profile.has_adviser = True
                contributor_profile.advisers_profile = form.cleaned_data.get('adviser')
            topics = form.cleaned_data.get('area_of_expertise')
            contributor_profile.save()
            for t in topics:
                contributor_profile.expertise_topics.add(t)
            #Remove an instance of saved contributor form information if it exists
            previous_form = ContributorProfileUnfinished.objects.filter(user_profile_id=user_prof.id).first()
            if previous_form:
                print("yes, previous form")
                curr_topics = previous_form.expertise_topics.all()
                for each_topic in curr_topics:
                    try:
                        previous_form.expertise_topics.remove(each_topic)
                    except ObjectDoesNotExist:
                        pass
                AcademicProfileUnfinished.objects.filter(contributor_profile=previous_form.id).delete()
                ContributorCertificationUnfinished.objects.filter(contributor_profile=previous_form.id).delete()
                OrganizationalAffiliationUnfinished.objects.filter(contributor_profile=previous_form.id).delete()
                AddressUnfinished.objects.filter(id=previous_form.address_id).delete()
                previous_form.delete()
            # @US_TODO: Remove this after Beta
            if (not BETA):
                pending_contributors = PendingContributors(contributor=contributor_profile)
                user_prof.is_pending_contributor = True
                pending_contributors.save()
                user_prof.save()
                # Setting up confirmation email.
                user_name = user.first_name + user.last_name
                user_email = user.email
                template = get_template('contributor_confirmation_email.html')
                context = Context({'userName': user_name,
                                   'email': user_email})
                content = template.render(context)
                email_message = EmailMessage('Your contributor application is under review', content,
                                             'relevate@outlook.com', [user_email],
                                             headers={'Reply-To': 'relevate@outlook.com'})
                email_message.content_subtype = "html"
                try:
                    email_message.send()
                except:
                    messages.error(request, 'Email could not be sent')
                # confirmation email sent.
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
                              'academics_req': academics_req,
                              'tag_names': Topics.objects.all().order_by('name'),
                              # 'institute': WORLD_UNIVERSITIES_LISTS[0:30], @TODO might need to use own database eventually
                          })

class ContributorTempSaveView(LoginRequiredMixin, View):
    """
    Contains LoginRequiredMixin
    """

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
        #look to see if the user has saved an unfinished contributor form already
        previous_form = ContributorProfileUnfinished.objects.filter(user_profile_id=user_prof.id).first()
        #TO_DO: change this so that instead of deleting old save info, it will be updated instead, updating is faster.
        if previous_form:
            print("yes, previous form")
            curr_topics = previous_form.expertise_topics.all()
            for each_topic in curr_topics:
                try:
                    previous_form.expertise_topics.remove(each_topic)
                except ObjectDoesNotExist:
                    pass
            AcademicProfileUnfinished.objects.filter(contributor_profile=previous_form.id).delete()
            ContributorCertificationUnfinished.objects.filter(contributor_profile=previous_form.id).delete()
            OrganizationalAffiliationUnfinished.objects.filter(contributor_profile=previous_form.id).delete()
            AddressUnfinished.objects.filter(id=previous_form.address_id).delete()
            previous_form.delete()
        academics_req = request.POST.get('hiddenAcaTable')
        print ("academic_req ", academics_req)
        cert_req = request.POST.get('certificateList')
        print ("cert req ", cert_req)
        affiliation_req = request.POST.get('affiliationList')
        print("affiliation_list", affiliation_req)
        x = request.POST.get('x')
        y = request.POST.get('y')
        w = request.POST.get('width')
        h = request.POST.get('height')
        avatar = request.POST.get('avatar')
        address = AddressUnfinished(
            street_address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zipcode=request.POST.get('zipcode'),
            country=request.POST.get('country')
        )
        address.save()
        contributor_profile = ContributorProfileUnfinished(
            user_profile=user_prof,
            website_url=request.POST.get('website_url'),
            cv=request.POST.get('cv'),
            biography_text=request.POST.get('biography'),
            address=address,
            interests=request.POST.get('interests'),
            avatar=request.POST.get('avatar'),
            accept_terms=False,
        )
        if (request.POST.get('avatar')):
            # Gets the original image to be cropped
            photo = Image.open(request.POST.get('avatar'))
            # Crops the image using values x,y,w,and h from the form
            cropped_image = photo.crop((x, y, w + x, h + y))
            # Splits the file name and the extension
            filename, file_extension = os.path.splitext(os.path.basename(urlparse(contributor_profile.avatar.url).path))
            cropped_image.save(settings.BASE_DIR + "/media/user_profiles/avatar/" + filename + file_extension)
            contributor_profile.avatar = "user_profiles/avatar/" + filename + file_extension
        topics = request.POST.getlist('area_of_expertise')
        contributor_profile.save()
        if topics:
            for t in topics:
                contributor_profile.expertise_topics.add(t)
        contributor_profile.save()
        message = 'Application has been saved.'
        unfinished_contributor_qualification(academics_req, cert_req, affiliation_req, contributor_profile)
        return HttpResponse(json.dumps({'message': message}))

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
        topics = user_prof.topics_preferences.all()
        user_already_sel = []
        for t in topics:
            user_already_sel.append(t)
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
        organizational_affiliations = OrganizationalAffiliation.objects.filter(
            contributor_profile=contributor_profile)
        max_academic_id = get_max_academic_id(academic_profile)
        contribution_form = ContributorUpdateForm({
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
            'accept_terms': True,
            'first_name': user.first_name,
            'last_name': user.last_name,
            "email": user.email,
            'password1': user.password,
            'password2': user.password,
            'area_of_expertise_user': user_already_sel,
        }, data_list=organization_list)
        obj = {
            'form': contribution_form,
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
        user_prof = UserProfile.objects.get(user=request.user)
        cp = ContributorProfile.objects.get(user_profile=user_prof)
        academics_req = request.POST.get('hiddenAcaTable')
        cert_req = request.POST.get('certificateList')
        org_req = request.POST.get('affiliationList')
        is_academics_and_cert_valid = validate_academic_and_cert(academics_req, request)
        print("here are errors!!!!!!!!!")
        print (form.errors)
        if form.is_valid() and is_academics_and_cert_valid:
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            avatar = form.cleaned_data.get('avatar')
            # Update User name, email
            user_prof.user.first_name = form.cleaned_data.get('first_name')
            user_prof.user.last_name = form.cleaned_data.get('last_name')
            user_prof.user.email = form.cleaned_data.get('email')
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
        if (user_prof.is_contributor or user_prof.is_pending_contributor):
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
                              "user":user,
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

        #Check if contributor id provided maps to existing contributor profile
        try:
            contributor_prof = ContributorProfile.objects.get(id=contrib_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse_lazy('contribution:home'))

        expertise_topics = contributor_prof.expertise_topics.all().order_by('name')
        academic_prof = AcademicProfile.objects.filter(contributor_profile=contributor_prof)
        certifications = ContributorCertification.objects.filter(contributor_profile=contributor_prof)
        organizational_affiliations = OrganizationalAffiliation.objects.filter(contributor_profile=contributor_prof)
        highest_ranking_degree = get_contributor_highest_degree(academic_prof)
        contrib_prof = ContributorProfile.objects.get(id=contrib_id)
        #Check if contributor profile is confirmed and viewable to public
        if contrib_prof.is_approved:
            return render(request, 'public_contributor_profile.html',
                  {
                      'user_prof': user_prof,
                      'contributor_prof': contributor_prof,
                      'contrib_prof': contrib_prof,
                      'expertise_topics': expertise_topics,
                      "academic_prof": academic_prof,
                      "certifications": certifications,
                      "highest_ranking_degree": highest_ranking_degree,
                      'organizational_affiliations': organizational_affiliations
                  })
        #If not, return to home page
        return HttpResponseRedirect(reverse_lazy('contribution:home'))


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
            if (user_prof.is_contributor):
                    contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
                    return render(request, 'contributors.html',
                                  {
                                      'user_prof': user_prof,
                                      'contrib_prof': contrib_prof,
                                      'contributors': get_list_of_contributor_credentials(contributor_profiles),
                                  })
            else:
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
        user_prof.is_pending_contributor = False
        user_prof.save()
        contrib_prof.is_approved = True
        contrib_prof.save()
        PendingContributors.objects.filter(contributor_id=contrib_prof.id).delete()
        return HttpResponse('')

class RequestRevisonButtonView(View):
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
        PendingContributors.objects.filter(contributor_id=contrib_prof.id).delete()
        denial = DeniedContributors(contributor=contrib_prof,
                                    date_denied=dt.utcnow(),
                                    reason=reason)
        denial.save()
        # @US_TODO: Send an email here upon denial
        user_name = user_prof.user.first_name + user_prof.user.last_name
        user_email = user_prof.user.email
        template = get_template('contributor_temp_denied_email.html')
        context = Context({'userName': user_name,
                           'email': user_email,
                           'reason': reason})
        content = template.render(context)
        email_message = EmailMessage('Relevate requests that you edit your contributor application', content,
                                     'relevate@outlook.com', [user_email],
                                     headers={'Reply-To': 'relevate@outlook.com'})
        email_message.content_subtype = "html"
        try:
            email_message.send()
        except:
            messages.error(request, 'Email could not be sent')
        # confirmation email sent.
        messages.success(request, 'Temp Email has been sent.')
        return HttpResponse("")


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
        user_prof.is_pending_contributor = False
        # Should we delete profiles that are permanently denied?
        # contrib_prof.delete()
        user_prof.save()
        print("Denying User: " + user_prof.user.first_name + " " + user_prof.user.last_name)
        PendingContributors.objects.filter(contributor_id=contrib_prof.id).delete()
        denial = DeniedContributors(contributor=contrib_prof,
                                    date_denied=dt.utcnow(),
                                    reason=reason)
        denial.save()
        # @US_TODO: Send an email here upon denial
        user_name = user_prof.user.first_name + user_prof.user.last_name
        user_email = user_prof.user.email
        template = get_template('contributor_denied_email.html')
        context = Context({'userName': user_name,
                           'email': user_email,
                           'reason': reason})
        content = template.render(context)
        email_message = EmailMessage('Your contributor application has been denied', content,
                                     'relevate@outlook.com', [user_email],
                                     headers={'Reply-To': 'relevate@outlook.com'})
        email_message.content_subtype = "html"
        try:
            email_message.send()
        except:
            messages.error(request, 'Email could not be sent')
        # confirmation email sent.
        messages.success(request, 'Email has been sent.')
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
