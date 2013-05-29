from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

class Blog(models.Model):
	STATECHOICE = (
	(0, 'Unpublished'),
	(1, 'Published'),
	(2, 'Deleted'),)
	publish_state = models.IntegerField(choices=STATECHOICE)
	
	
	title = models.CharField(max_length=200)
	date_created = models.DateTimeField('date created')
	author = models.ForeignKey(User)
	def delete(self):
		self.publish_state = "deleted"
	def publish(self):
		self.publish_state = "published"
	def __unicode__(self):
		return self.title

class Entry(models.Model):
	blog = models.ForeignKey(Blog)
	title = models.CharField(max_length=200)
	original_pub_date = models.DateTimeField('date published')
	def __unicode__(self):
		return self.title

class Comment(MPTTModel):
	""" Threaded comments for blog posts """
	entry = models.ForeignKey(Entry)
	author = models.ForeignKey(User)
	comment = models.TextField()
	added  = models.DateTimeField(default=datetime.datetime.now())
	# a link to comment that is being replied, if one exists
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	def __unicode__(self):
		return self.entry.title + " - " + self.comment

	class MPTTMeta:
		# comments on one level will be ordered by date of creation
		order_insertion_by=['added']



class Revision(models.Model):
	body = models.TextField()
	entry = models.ForeignKey(Entry)
	version_number = models.IntegerField(default=0)
	pub_date = models.DateTimeField('date published')

	def save(self, *args, **kwargs):
		# Only modify number if creating for the first time (is default 0)
		if self.version_number == 0:
			# Grab the highest current index (if it exists)
			try:
				recent = Revision.objects.filter(entry__exact=self.entry).order_by('-version_number')[0]
				self.version_number = recent.version_number + 1
			except IndexError:
				self.version_number = 1
		# Call the "real" save() method
		super(Revision, self).save(*args, **kwargs)
		c = CurrentVersion(entry=self.entry, current_version=self)
		c.save()

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	def __unicode__(self):
		return self.body

class CurrentVersion(models.Model):
	entry = models.OneToOneField(Entry, primary_key=True)
	current_version = models.OneToOneField(Revision)

	def save(self, *args, **kwargs):
		if len(CurrentVersion.objects.filter(entry__exact=self.entry))>0:
			kwargs['force_update'] = True
			kwargs['force_insert'] = False
		else:
			kwargs['force_insert'] = True
			kwargs['force_update'] = False
		return super(CurrentVersion, self).save(*args, **kwargs)


	



