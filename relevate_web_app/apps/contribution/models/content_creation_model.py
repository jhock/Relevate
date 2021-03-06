from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class ContentCreation(models.Model):
    """
    +--------------------------+-------------------------------------------------------------------------+
    |      Property            |                                   Use                                   |
    +==========================+=========================================================================+
    | image                    | A url pointer to the location of the post image                         |
    +--------------------------+-------------------------------------------------------------------------+
    | title                    | Title of the post                                                       |
    +--------------------------+-------------------------------------------------------------------------+
    | content                  | The post content                                                        |
    +--------------------------+-------------------------------------------------------------------------+
    | blurb                    | A short excerpt of the post content                                     |
    +--------------------------+-------------------------------------------------------------------------+
    | references               | A place to list any references used in the post                         |
    +--------------------------+-------------------------------------------------------------------------+
    | contributor              | link to a contributor profile                                           |
    +--------------------------+-------------------------------------------------------------------------+
    | slug                     | unique slug identifier based on time created                            |
    +--------------------------+-------------------------------------------------------------------------+
    | isPublished              | Field to set Post as published or unpublished                           |
    +--------------------------+-------------------------------------------------------------------------+
    | type                     | Type field using TYPE_OF_CONTENT list                                   |
    +--------------------------+-------------------------------------------------------------------------+
    | level                    | Level field using LEVEL_OF_EXPERIENCE list                              |
    +--------------------------+-------------------------------------------------------------------------+
    | layout                   | Determines the layout on the individual viewing page                    |
    +--------------------------+-------------------------------------------------------------------------+
    |  public_scholarship_or_content_creation  | Boolean, True is public_scholarship, False is content_c |
    +--------------------------+-------------------------------------------------------------------------+

    model for the Content Creation page.
    """
    class Meta:
        db_table = 'content_creation'

    image = models.ImageField(upload_to='content_creation/images', null=True, blank=True)
    title = models.TextField(max_length=1000)
    content = RichTextUploadingField(null=True, blank=True)
    blurb = models.CharField(max_length=500, default="")
    content_file = models.FileField(upload_to='content_creation/files', null=True, blank=True)
    references = models.TextField(max_length=3000, null=True, blank=True)
    contributor = models.ForeignKey('profiles.ContributorProfile', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(default=None, max_length=100)
    isPublished = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


    type = models.CharField(max_length=30)
    level = models.CharField(max_length=30)
    layout = models.CharField(max_length=30)
    public_scholarship_or_content_creation = models.BooleanField(default=False)

    createdDate = models.DateTimeField(default=datetime.utcnow)
    publishedDate = models.DateTimeField(null=True, blank=True)
    updatedDate = models.DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        if not self.slug:
            title = self.title
            slug_val = title + str(self.createdDate)
            self.slug = slugify(slug_val)
        super(ContentCreation, self).save(*args, **kwargs)