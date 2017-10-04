from django.contrib import admin
from .models.topic_model import Topics
from .models.article_model import Article
from .models.link_model import Link
from .models.post_model import Post
from .models.infographic_model import Infographic
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib import admin
from .models.about_person_model import AboutPerson

def roles(self):
    #short_name = unicode # function to get group name
    short_name = lambda x:str(x)[:1].upper() # first letter of a group
    p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x)) for x in self.groups.all()])
    if self.user_permissions.count(): p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)
roles.allow_tags = True
roles.short_description = u'Groups'

def adm(self):
    return self.is_superuser
adm.boolean = True
adm.admin_order_field = 'is_superuser'

def staff(self):
    return self.is_staff
staff.boolean = True
staff.admin_order_field = 'is_staff'

from django.core.urlresolvers import reverse
def persons(self):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in self.user_set.all().order_by('username')])
persons.allow_tags = True

class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', staff, adm, roles]
    list_filter = ['groups', 'is_staff', 'is_superuser', 'is_active']

class GroupAdmin(GroupAdmin):
    list_display = ['name', persons]
    list_display_links = ['name']


class AboutPersonAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/jquery-3.1.1.min.js',
            'js/jquery-ui.min.js',
            'js/admin-list-reorder.js',
        )
    list_display = ['name', 'createdDate', 'position', 'funder_or_adviser']
    list_editable = ['position']  # 'position' is the name of the model field which holds the position of an element

admin.site.register(AboutPerson, AboutPersonAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)

# Register your models here.
admin.site.register(Topics)
admin.site.register(Article)
admin.site.register(Link)
admin.site.register(Post)
admin.site.register(Infographic)