# SEO Action Plan: Optimize H1 Tags for Better Keyword Targeting

**Priority**: HIGH (Month 1)  
**Effort**: LOW  
**Expected Impact**: MEDIUM-HIGH

---

## Overview

Update H1 tags on key pages to include location + service keywords to improve search relevance and rankings.

---

## Pages to Update

### 1. Treatments Page (`/treatments.html`)

**File**: `SimpleSites/content/pages/en/treatments.md`

**Current H1**: "Holistic Treatment Offerings"

**New H1**: "Traditional Chinese Medicine Treatments in New Westminster"

**Action**:
```yaml
# In treatments.md frontmatter or content:
intro:
  title: "Traditional Chinese Medicine Treatments in New Westminster"
```

---

### 2. Therapists Page (`/therapists.html`)

**File**: `SimpleSites/content/pages/en/therapists.md`

**Current H1**: "Eva Fang Yuan"

**New H1**: "Dr. Eva Fang Yuan - Licensed Acupuncturist in New Westminster"

**Action**:
Update the therapist name/title in the template or content to include credentials and location.

**Note**: The H1 is currently in the template at line ~238. May need to adjust template logic or add a page-level H1 field.

---

### 3. Contact Page (`/contact.html`)

**File**: `SimpleSites/content/pages/en/contact.md`

**Current H1**: "Visit Us"

**New H1**: "Contact Hope TCM Clinic in New Westminster"

**Action**:
```yaml
# In contact.md:
intro:
  title: "Contact Hope TCM Clinic in New Westminster"
```

---

## Chinese Version Updates

Don't forget to update the Chinese versions as well:
- `SimpleSites/content/pages/cn/treatments.md`
- `SimpleSites/content/pages/cn/therapists.md`
- `SimpleSites/content/pages/cn/contact.md`

**Chinese H1 Examples**:
- Treatments: "新西敏市中醫治療服務" (TCM Treatments in New Westminster)
- Therapists: "袁芳醫生 - 新西敏市註冊針灸師"
- Contact: "聯絡新西敏市向陽中醫診所"

---

## Why This Matters

H1 tags are one of the strongest on-page SEO signals:
- They tell search engines the main topic of the page
- Including location ("New Westminster") + service ("Acupuncturist", "TCM") helps with local SEO
- Makes it clear to both users and search engines what the page is about

---

## Implementation Steps

1. Open each content markdown file
2. Locate the H1 (usually in `intro.title` or similar frontmatter field)
3. Update with keyword-rich version
4. Test locally to ensure it displays correctly
5. Deploy changes

---

## Testing

After deployment:
1. Visit each page and verify H1 displays correctly
2. Check that it looks good on mobile
3. Use browser inspector to confirm only ONE H1 per page
4. Monitor Google Search Console for ranking changes

---

## Success Metrics

- ✅ All 3 pages have keyword-optimized H1s
- ✅ Chinese versions updated
- ✅ Each page has exactly one H1
- ✅ H1s are visible and display correctly on all devices

---

## Timeline

**Estimated Time**: 30 minutes
- English pages: 15 min
- Chinese pages: 15 min

**Target Completion**: Month 1 (Quick Wins phase)
