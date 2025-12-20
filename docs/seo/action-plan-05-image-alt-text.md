# SEO Action Plan: Add Image Alt Text with Keywords

**Priority**: HIGH (Month 1)  
**Effort**: LOW  
**Expected Impact**: MEDIUM

---

## Overview

Add descriptive alt text to all images on the website that includes location + service keywords for better accessibility and image search visibility.

---

## Current Status

Some images may have alt text, but it likely doesn't include SEO keywords or location information.

---

## Action Items

### Homepage Images

**File**: `SimpleSites/content/pages/en/index.md`

**Hero Image** (`/images/Inner-Chinese.jpg`):
- Current: May be generic or missing
- **New**: `"Traditional Chinese Medicine acupuncture clinic interior at Hope TCM in New Westminster BC"`

### Therapists Page

**File**: `SimpleSites/content/pages/en/therapists.md` or template

**Dr. Eva's Photo** (`/images/Eva.jpg`):
- Currently: `"Eva Fang Yuan - Doctor of TCM | R.Ac."`
- **Enhanced**: `"Dr Eva Fang Yuan registered acupuncturist and TCM doctor at Hope Clinic in New Westminster"`

### Treatment Pages

**Files**: Individual treatment markdown files

**Treatment Images** (if any):
- Acupuncture needles: `"Acupuncture needles for pain relief and stress management at Hope TCM Clinic New Westminster"`
- Cupping therapy: `"Cupping therapy treatment for muscle pain in New Westminster"`
- Herbal medicine: `"Traditional Chinese herbal formulas and remedies at Hope TCM"`

### Logo

**File**: Template navigation section

**Logo Image** (`/images/logo.png`):
- Current: `"Hope Traditional Chinese Medicine Clinic"`
- **Enhanced**: `"Hope Traditional Chinese Medicine Clinic logo - Acupuncture and TCM in New Westminster BC"`

---

## Implementation Guide

### Method 1: In Markdown Content Files

If images are referenced in markdown content:
```markdown
![Dr Eva Fang Yuan registered acupuncturist New Westminster](/images/Eva.jpg)
```

### Method 2: In HTML Templates

If images are in templates:
```html
<img src="/images/Eva.jpg" 
     alt="Dr Eva Fang Yuan registered acupuncturist and TCM doctor in New Westminster" 
     width="..." 
     height="...">
```

### Method 3: In YAML Frontmatter

If image paths are in frontmatter:
```yaml
therapist:
  image: "/images/Eva.jpg"
  image_alt: "Dr Eva Fang Yuan registered acupuncturist New Westminster"
```

---

## Alt Text Best Practices

✅ **Good Alt Text**:
- Descriptive and specific
- Includes relevant keywords naturally
- Mentions location when relevant
- 125 characters or less (optimal)
- Describes what's IN the image

❌ **Avoid**:
- Keyword stuffing: "acupuncture acupuncture TCM acupuncture New Westminster"
- "Image of..." or "Picture of..." (screen readers already say "image")
- Overly long descriptions (>150 characters)
- Using same alt text for different images

---

## Keyword Integration Formula

**Format**: `[What's shown] + [Service/Treatment] + [Location]`

**Examples**:
- `"Acupuncture needle insertion for pain relief in New Westminster"`
- `"Chinese herbal medicine dispensary at Hope TCM Clinic"`
- `"Cupping therapy marks on patient back for muscle tension relief"`

---

## Audit Checklist

### Homepage
- [ ] Hero image has descriptive alt text
- [ ] Logo has alt text with clinic name and location
- [ ] Any service icons have alt text

### Therapists Page
- [ ] Dr. Eva's photo has alt text with credentials + location
- [ ] Specialization icons (if any images)

### Treatment Pages
- [ ] Each treatment detail page has alt text for images
- [ ] Treatment process images described

### Contact Page
- [ ] Map or location images have alt text
- [ ] Any instructional images (buzzer video thumbnail)

### Blog Posts
- [ ] Featured images have descriptive alt text
- [ ] Inline images in articles

---

## Testing

1. **Manual Review**: Right-click images → Inspect → Check alt attribute
2. **Screen Reader Test**: Use NVDA (Windows) or VoiceOver (Mac) to test
3. **SEO Tools**: 
   - Use Lighthouse audit in Chrome DevTools
   - Check Google Search Console for image indexing

---

## Success Metrics

- ✅ All images have descriptive alt text
- ✅ No accessibility warnings for missing alt text
- ✅ Alt text includes relevant keywords naturally
- ✅ Images begin appearing in Google Image Search

---

## Timeline

**Estimated Time**: 1-2 hours
- Image audit: 30 min
- Writing alt text: 30 min
- Implementation: 30 min
- Testing: 30 min

**Target Completion**: Month 1 (Quick Wins)

---

## Tools & Resources

- [WebAIM Alt Text Guide](https://webaim.org/techniques/alttext/)
- Chrome DevTools Lighthouse (Accessibility audit)
- Google Search Console (Image indexing status)
