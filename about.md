---
layout: page
permalink: /about/index.html
title: Neurostorm
tags: [background, summary]
imagefeature: globalbrain.jpg
chart: true
---
<figure>
  <img src="{{ site.url }}/images/globalbrain.jpg" alt="Neuro Cloud Consortium" style='width:20%; border-radius:50%'>
</figure>

{% assign total_words = 0 %}
{% assign total_readtime = 0 %}
{% assign featuredcount = 0 %}
{% assign statuscount = 0 %}

{% for post in site.posts %}
    {% assign post_words = post.content | strip_html | number_of_words %}
    {% assign readtime = post_words | append: '.0' | divided_by:200 %}
    {% assign total_words = total_words | plus: post_words %}
    {% assign total_readtime = total_readtime | plus: readtime %}
    {% if post.featured %}
    {% assign featuredcount = featuredcount | plus: 1 %}
    {% endif %}
{% endfor %}


We are **Neurostorm**, and we are working towards a global ecosystem for neuroscience research. This website serves as a blog and contains documentation, press, updates, and tutorials.

> Neurostorm brings neuroscience from the bench to the web.

Whether through education, experimental design, data processing, or analysis and discovery, all are encouraged to participate. Neurostorm facilitates the scientific process and lowers the barrier to entry for accessing data and performing sophisticated computation.

<figure class="full">
	<a href="{{ site.url }}/images/about/neurostorm_framework.png"><img src="{{ site.url }}/images/about/neurostorm_framework.png"></a>
	<figcaption>Scientific model under Neurostorm</figcaption>
</figure>

<!-- <figure class="half">
	<a href="{{ site.url }}/images/about/scientific_model.png"><img src="{{ site.url }}/images/about/scientific_model.png"></a>
	<a href="{{ site.url }}/images/about/sic_framework.png"><img src="{{ site.url }}/images/about/sic_framework.png"></a>
</figure> -->


## Site Stats

| item | value |
|:-----|:------|
| Number of posts | {{ site.posts | size }} |
| Number of active categories | {{ site.categories | size }} |
| Number of words | {{ total_words }} | 
| Estimated reading time (at {{ site.wpm }} WPM) | <span class="time">{{ total_readtime }}</span> minutes |
| Number of featured posts | {{ featuredcount }} | 
| Date of most recent post |  {% for post in site.posts limit:1 %}{% assign modifiedtime = post.modified | date: "%Y%m%d" %}{% assign posttime = post.date | date: "%Y%m%d" %}<time datetime="{{ post.date | date_to_xmlschema }}" class="post-time">{{ post.date | date: "%d %b %Y" }}</time>{% if post.modified %}{% if modifiedtime != posttime %} and last modified on <time datetime="{{ post.modified | date: "%Y-%m-%d" }}" itemprop="dateModified">{{ post.modified | date: "%d %b %Y" }}</time>{% endif %}{% endif %}{% endfor %}. |
| Date of last commit  | {{ site.time | date: "%A, %d %b %Y" }} at {{ site.time | date: "%I:%M %p" }} [UTC](http://en.wikipedia.org/wiki/Coordinated_Universal_Time "Temps Universel Coordonné") |

<!-- <figure class="third">
	<a href="{{ site.url }}/images/about/1.jpg"><img src="{{ site.url }}/images/about/1-001.jpg"></a>
	<a href="{{ site.url }}/images/about/2.jpg"><img src="{{ site.url }}/images/about/2-001.jpg"></a>
	<a href="{{ site.url }}/images/about/3.jpg"><img src="{{ site.url }}/images/about/3-001.jpg"></a>
</figure> -->
