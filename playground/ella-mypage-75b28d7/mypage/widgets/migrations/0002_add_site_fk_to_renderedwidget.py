
from south.db import db
from django.db import models
from mypage.widgets.models import *
import datetime

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'RenderedWidget.site'
        db.add_column('widgets_renderedwidget', 'site', models.ForeignKey(orm['sites.Site'], default=1), keep_default=False)
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'RenderedWidget.site'
        db.delete_column('widgets_renderedwidget', 'site_id')
        
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'widgets.renderedwidget': {
            'Meta': {'unique_together': "(('widget','state',),)"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'rendered_html': ('models.TextField', [], {}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {}),
            'state': ('models.SmallIntegerField', [], {'default': '0'}),
            'widget': ('models.ForeignKey', ["orm['widgets.Widget']"], {'verbose_name': "_('Widget')"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'widgets.widget': {
            'content_type': ('ContentTypeField', [], {'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'last_downloaded': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'next_download': ('models.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'shared': ('models.BooleanField', ["_('Shared')"], {'default': 'True'}),
            'slug': ('models.SlugField', [], {'max_length': '100'}),
            'title': ('models.CharField', ["_('Title')"], {'max_length': '100'}),
            'url': ('models.URLField', ["_('Header link URL')"], {'blank': 'True'})
        }
    }
    
    complete_apps = ['widgets']
