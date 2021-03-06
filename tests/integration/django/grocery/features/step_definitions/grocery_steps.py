# -*- coding: utf-8 -*-
import urllib2
from lettuce import step, before, world
from lettuce.django import django_url
from nose.tools import assert_equals

@before.each_scenario
def prepare_the_world(scenario):
    world.statuses = []
    world.content_types = []

@step(u'Given I fetch the urls:')
def given_i_fetch_the_urls(step):
    urls = map(lambda i: django_url(i['url']), step.hashes)
    for url in urls:
        try:
            http = urllib2.urlopen(url)
        except Exception, http:
            pass

        world.statuses.append((url, http.code))
        world.content_types.append((url, http.headers.dict['content-type']))
        http.close()

@step(u'When all the responses have status code 200')
def when_all_the_responses_have_status_code_200(step):
    for url, status in world.statuses:
        assert status is 200, 'for %s the status code should be 200 but is %d' % (url, status)

@step(u'Then all the responses have mime type "(.*)"')
def then_all_the_responses_have_mime_type_group1(step, group1):
    for url, content_type in world.content_types:
        assert_equals(content_type, group1, 'failed at %s' % url)
