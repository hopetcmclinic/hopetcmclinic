# SEO Action Plan: Enhance Internal Linking Structure

**Priority**: HIGH (Month 2)  
**Effort**: LOW  
**Expected Impact**: MEDIUM

---

## Overview

Improve internal linking to help search engines crawl your site better and pass SEO value between pages.

---

## Linking Strategies

### 1. From Treatments Page to Individual Treatment Pages

**File**: `SimpleSites/content/pages/en/treatments.md`

**Current Issue**: The word "Acupuncture" appears but isn't linked to the detailed acupuncture page.

**Action**: Link key treatment terms to their detail pages:
- "Acupuncture" → `/treatments/acupuncture.html`
- "Facial Rejuvenation Acupuncture" → `/treatments/facial-rejuvenation-acupuncture.html`
- "Fu's Subcutaneous Needling" → link to blog post
- "Cupping", "Moxibustion", "Gua Sha" → respective treatment pages

---

### 2. From Homepage FAQ to Treatment Pages

**File**: `SimpleSites/content/pages/en/index.md`

**Current**: FAQ answers mention treatments but links are minimal

**Action**: Add contextual links in FAQ answers:
```yaml
faq:
  entries:
    - q: "What can I expect during treatment?"
      a: "For more details on each type of treatment, please visit our <a href=\"/treatments.html\">Treatments</a> page or learn about specific treatments like <a href=\"/treatments/acupuncture.html\">Acupuncture</a> and <a href=\"/treatments/cupping.html\">Cupping</a>."
```

---

### 3. Cross-link Treatment Pages

**Files**: All treatment detail pages

**Action**: Add "Related Treatments" section at the bottom of each treatment page:

```markdown
## Related Treatments

You may also be interested in:
- [Facial Rejuvenation Acupuncture](/treatments/facial-rejuvenation-acupuncture.html)
- [Cupping Therapy](/treatments/cupping.html)
- [Herbal Formulas](/treatments/herbal-formulas.html)
```

---

### 4. Blog-to-Service Links

**Files**:
- Blog posts in `SimpleSites/content/articles/`

**Action**: Ensure each blog post links to at least 1-2 relevant service pages:

- "Deep Relaxation & Restorative Sleep" → link to `/treatments/acupuncture.html`
- "Fu's Subcutaneous Needling" → link to `/treatments/acupuncture.html`
- "Traditional Chinese Medicine" → link to `/treatments.html`

---

## Implementation Checklist

### Homepage (`index.md`)
- [ ] Add links in FAQ answers to treatment pages
- [ ] Link treatment names in intro section

### Treatments Overview (`treatments.md`)
- [ ] Link "Acupuncture" to detail page
- [ ] Link "Facial Rejuvenation Acupuncture" to detail page
- [ ] Link all complementary modalities
- [ ] Link technique mentions (Fu's Needling) to blog

### Treatment Detail Pages
- [ ] Add "Related Treatments" section to each page
- [ ] Cross-link to complementary treatments
- [ ] Link back to main treatments page

### Blog Posts
- [ ] Ensure each links to 1-2 service pages
- [ ] Add CTAs to book appointments

---

## Testing

After implementation:
1. Click through all links to ensure they work
2. Check that links open in same tab (not new tab for internal links)
3. Verify anchor text is descriptive (not "click here")
4. Use a tool like Screaming Frog to crawl your site and verify all internal links

---

## Best Practices

✅ **Do**:
- Use descriptive anchor text ("Acupuncture treatment" not "click here")
- Link to relevant, helpful pages
- Keep it natural - don't force links

❌ **Don't**:
- Over-optimize anchor text  (don't use "Acupuncture New Westminster" every time)
- Link every instance of a keyword
- Create circular links (A→B→A with no value)

---

## Success Metrics

- ✅ Each main page links to 3-5 relevant internal pages
- ✅ All blog posts link to at least 1 service page
- ✅ No broken internal links
- ✅ Reduced bounce rate (users explore more pages)

---

## Timeline

**Estimated Time**: 2 hours
- Homepage updates: 20 min
- Treatments page updates: 20 min
- Treatment detail pages: 60 min
- Blog posts: 20 min

**Target Completion**: Month 2
