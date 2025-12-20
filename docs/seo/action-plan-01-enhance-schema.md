# SEO Action Plan: Enhance Structured Data (Schema Markup)

**Priority**: HIGH  
**Effort**: MEDIUM  
**Expected Impact**: HIGH

---

## Overview

Enhance existing schema markup on the therapists page and add FAQ schema to pages with FAQ sections to improve search result appearance and Rich Snippet eligibility.

---

## Tasks

### 1. Enhance Person Schema on Therapists Page

**Files to Edit**: 
- `SimpleSites/templates/pages/therapists.html` (or template that generates the schema)

**Current Schema** (lines ~407-422 in generated HTML):
```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "mainEntity": {
    "@type": "Person",
    "name": "Eva Fang Yuan",
    "description": "Registered Acupuncturist and Doctor of TCM",
    "image": "..."
  }
}
```

**Action**:
Add these properties to the Person schema:
- `jobTitle`: "Doctor of Traditional Chinese Medicine & Registered Acupuncturist"
- `alumniOf`: Object with Tzu Chi College
- `memberOf`: Object with CCHPBC
- `knowsAbout`: Array of all specializations from page
- `worksFor`: Link to clinic

**Expected Code**:
```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "dateCreated": "2023-11-01T00:00:00-05:00",
  "dateModified": "2025-12-20T00:00:00-08:00",
  "mainEntity": {
    "@type": "Person",
    "name": "Eva Fang Yuan",
    "alternateName": "Eva",
    "jobTitle": "Doctor of Traditional Chinese Medicine & Registered Acupuncturist",
    "description": "Registered Acupuncturist and Doctor of TCM specializing in fertility, chronic pain, and digestive health",
    "image": "https://www.hopetcmclinic.ca/images/Eva.jpg",
    "alumniOf": {
      "@type": "Organization",
      "name": "Tzu Chi International College of Traditional Chinese Medicine"
    },
    "memberOf": {
      "@type": "Organization",
      "name": "College of Complementary Health Professionals of BC",
      "sameAs": "https://cchpbc.ca"
    },
    "knowsAbout": [
      "Digestive Issues", 
      "Irritable Bowel Syndrome",
      "Insomnia", 
      "Infertility", 
      "Chronic Pain",
      "Menstrual Disorders",
      "Menopause",
      "Emotional Imbalances",
      "Traditional Chinese Medicine",
      "Acupuncture"
    ],
    "worksFor": {
      "@type": "MedicalClinic",
      "name": "Hope Traditional Chinese Medicine Clinic"
    }
  }
}
```

---

### 2. Add Service Schema to Treatment Pages

**Files to Create/Edit**:
- Each individual treatment page template needs schema

**Pages Affected**:
- `/treatments/acupuncture.html`
- `/treatments/facial-rejuvenation-acupuncture.html`
- `/treatments/cupping.html`
- `/treatments/moxibustion.html`
- `/treatments/gua-sha.html`
- `/treatments/herbal-formulas.html`

**Action**:
Add `MedicalProcedure` schema to each treatment page.

**Example for Acupuncture page**:
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalProcedure",
  "name": "Acupuncture Treatment",
  "description": "Traditional acupuncture for pain relief, stress reduction, and holistic healing",
  "procedureType": "Acupuncture",
  "followup": "Follow-up sessions recommended for chronic conditions",
  "preparation": "Light meal 1-2 hours before treatment recommended",
  "howPerformed": "Ultra-thin sterile needles inserted at specific acupoints",
  "bodyLocation": "Various meridian points",
  "provider": {
    "@type": "MedicalClinic",
    "name": "Hope Traditional Chinese Medicine Clinic"
  }
}
```

---

### 3. Add FAQ Schema to Pages with FAQ Sections

**Files to Edit**:
- Homepage (`index.html`) - has FAQ section
- Treatments page (`treatments.html`) - has FAQ section
- Any treatment detail pages with FAQs

**Action**:
Add `FAQPage` schema with all Q&A pairs from the page.

**Example**:
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How many acupuncture treatments will I need?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "It varies by condition. Acute issues may resolve in 2-3 sessions, while chronic conditions often require ongoing care for reliable results."
      }
    },
    {
      "@type": "Question",
      "name": "Do you do direct billing?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We are registered acupuncturists, but do not do direct billing to MSP or insurance companies. A receipt will be issued after each session."
      }
    }
  ]
}
```

---

## Implementation Notes

**Where to add schema**:
- Look for where `_generate_structured_data()` is called in `builder.py`
- Schema should be added to the template context and rendered in `<script type="application/ld+json">` tags
- Can have multiple schema blocks on the same page

**Testing**:
1. After implementation, test schema using [Google Rich Results Test](https://search.google.com/test/rich-results)
2. Validate with [Schema.org Validator](https://validator.schema.org/)
3. Check Google Search Console for schema errors after deployment

---

## Success Metrics

- ✅ All schema passes validation (no errors)
- ✅ Rich Results Test shows eligible for rich snippets
- ✅ Enhanced search result appearance in SERPs within 2-4 weeks
- ✅ Potential increase in CTR from search results

---

## Timeline

**Estimated Time**: 3-4 hours
- Person schema enhancement: 30 min
- Service schema for 6 pages: 2 hours
- FAQ schema for 2-3 pages: 1 hour
- Testing and validation: 30 min

**Target Completion**: Month 2 (Content Foundation phase)
