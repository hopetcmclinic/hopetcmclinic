# SEO Action Plan: Enhance Structured Data (Schema Markup)

**Priority**: HIGH  
**Effort**: MEDIUM  
**Expected Impact**: HIGH

---

## Overview

Enhance existing schema markup on the therapists page and add FAQ schema to pages with FAQ sections to improve search result appearance and Rich Snippet eligibility.

---

## Completed Tasks ✅

### ✅ 1. Enhanced Person Schema on Therapists Page (Completed: Dec 20, 2025)

**Files Modified**: 
- `SimpleSites/templates/pages/therapists.html`

**Completion Details**:
- Added `jobTitle`, `alumniOf`, `memberOf`, `knowsAbout`, `worksFor` properties
- Updated `dateModified` to 2025-12-20
- Schema now includes comprehensive professional information and specializations

---

### ✅ 2. Added Service Schema to Treatment Pages (Completed: Dec 20, 2025)

**Files Modified**:
- `SimpleSites/templates/pages/article.html` - Added conditional MedicalProcedure schema block
- All 12 treatment page content files (6 English + 6 Chinese)

**Pages with MedicalProcedure Schema**:
- Acupuncture (EN + CN)
- Facial Rejuvenation Acupuncture (EN + CN)
- Cupping (EN + CN)
- Moxibustion (EN + CN)
- Gua Sha (EN + CN)
- Herbal Formulas (EN + CN)

**Completion Details**:
- Added `name`, `description`, `procedureType`, `preparation`, `howPerformed`, `followup` properties
- Schema metadata added to frontmatter of all treatment markdown files
- Chinese versions localized with Chinese-language schema content

---

### ✅ 3. Added FAQ Schema to Pages with FAQ Sections (Completed: Dec 20, 2025)

**Files Modified**:
- `SimpleSites/templates/pages/index.html` - Added FAQPage schema block
- `SimpleSites/templates/pages/treatments.html` - Added FAQPage schema block

**Pages with FAQ Schema**:
- Homepage (EN + CN) - 5 questions each
- Treatments page (EN + CN) - 5 questions each

**Completion Details**:
- FAQPage schema dynamically generates from `page.faq.entries` data
- Supports both English and Chinese versions automatically
- Uses `tojson` filter for proper JSON escaping
- Coexists with existing MedicalProcedure schema on treatments page
- All schemas validated and verified in browser

---

## Remaining Tasks

No remaining tasks - all schema enhancements complete!

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
