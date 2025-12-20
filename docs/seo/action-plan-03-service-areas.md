# SEO Action Plan: Add Service Areas Section to Contact Page

**Priority**: MEDIUM (Month 3)  
**Effort**: LOW  
**Expected Impact**: MEDIUM

---

## Overview

Add a "Service Areas" section to the contact page to capture search traffic from neighboring cities without creating duplicate content.

---

## Implementation

### File to Edit
`SimpleSites/content/pages/en/contact.md`

### Content to Add

Add this new section to the contact page (after the existing content, before the book section):

```markdown
---
# ... existing frontmatter ...
service_areas:
  title: "Service Areas"
  intro: "Hope TCM Clinic proudly serves patients throughout the Greater Vancouver area from our convenient New Westminster location."
  subtitle: "Easy Access From:"
  areas:
    - city: "Burnaby"
      desc: "Just one SkyTrain stop away on the Expo Line (Columbia Station to New Westminster Station - 8 minutes). Free parking available nearby."
    - city: "Coquitlam & Port Coquitlam"
      desc: "Quick 15-minute drive via Highway 1, or take the Evergreen Line to Lougheed, transfer to Millennium Line to Columbia, then Expo Line to New Westminster."
    - city: "Surrey"
      desc: "Approximately 30 minutes via Highway 1 or SkyTrain (Expo Line direct from Surrey Central)."
    - city: "Richmond"
      desc: "Cross the Queensborough Bridge for a scenic 20-minute drive, or take Canada Line to Broadway-City Hall, transfer to Millennium/Expo Line."
    - city: "Vancouver"
      desc: "Direct SkyTrain access via Expo Line from Downtown (Waterfront to New Westminster - 25 minutes)."
  footer: "We're located just 5 minutes walk from New Westminster SkyTrain Station, making us easily accessible for patients across Metro Vancouver."
---
```

### Template Update

**File**: `SimpleSites/templates/pages/contact.html`

Add this section to render the service areas:

```html
<!-- Service Areas Section -->
{% if page.service_areas %}
<div class="my-12">
    <h2 class="font-serif text-3xl font-bold text-primary mb-4">
        {{ page.service_areas.title }}
    </h2>
    <p class="text-lg text-slate-600 mb-6">
        {{ page.service_areas.intro }}
    </p>
    
    <h3 class="text-xl font-semibold text-slate-800 mb-4">
        {{ page.service_areas.subtitle }}
    </h3>
    
    <div class="space-y-4">
        {% for area in page.service_areas.areas %}
        <div class="p-4 bg-stone-50 rounded-lg border border-stone-200">
            <h4 class="font-bold text-primary mb-2">{{ area.city }}</h4>
            <p class="text-slate-600">{{ area.desc }}</p>
        </div>
        {% endfor %}
    </div>
    
    <p class="mt-6 text-slate-600 italic">
        {{ page.service_areas.footer }}
    </p>
</div>
{% endif %}
```

---

## Chinese Version

**File**: `SimpleSites/content/pages/cn/contact.md`

Add Chinese translation:

```yaml
service_areas:
  title: "服務地區"
  intro: "向陽中醫診所為大溫哥華地區的患者提供服務，診所位於交通便利的新西敏市。"
  subtitle: "便捷訪問："
  areas:
    - city: "本拿比 (Burnaby)"
      desc: "從本拿比搭乘博覽線僅需一站（Columbia站到New Westminster站 - 8分鐘）。附近有免費停車位。"
    - city: "高貴林和高貴林港 (Coquitlam & Port Coquitlam)"
      desc: "經1號公路駕車僅需15分鐘，或搭乘長青線到Lougheed，轉乘千禧線到Columbia，再轉博覽線到New Westminster。"
    - city: "素里 (Surrey)"
      desc: "經1號公路約30分鐘，或從Surrey Central搭乘博覽線直達。"
    - city: "列治文 (Richmond)"
      desc: "穿過皇后堡橋風景優美的20分鐘車程，或搭乘加拿大線到Broadway-City Hall，轉千禧線/博覽線。"
    - city: "溫哥華 (Vancouver)"
      desc: "從市中心搭乘博覽線直達（Waterfront到New Westminster - 25分鐘）。"
  footer: "我們距離New Westminster天車站僅5分鐘步行路程，方便大溫哥華地區患者就診。"
```

---

## SEO Benefits

**Keywords Naturally Included:**
- "Acupuncture Burnaby" (implied through context)
- "TCM Coquitlam"
- "Acupuncture Surrey"
- "Chinese Medicine Richmond"
- "New Westminster"
- "Greater Vancouver"

**Why This Works:**
1. Provides genuine value (transit/driving directions)
2. Natural keyword inclusion without keyword stuffing
3. No duplicate content risk
4. Single page to update and maintain
5. Helps with local search relevance

---

## Implementation Steps

1. Update `contact.md` (English) with service_areas frontmatter
2. Update `contact.md` (Chinese) with translated content
3. Update `contact.html` template to render the service areas section
4. Test locally to ensure proper rendering
5. Verify mobile responsiveness
6. Deploy changes

---

## Testing Checklist

- [ ] Service areas section displays on contact page
- [ ] All 5 cities listed with transit/driving directions
- [ ] Responsive on mobile devices
- [ ] Chinese version displays correctly
- [ ] No layout issues or text overflow
- [ ] Links properly (if any transit authority links added)

---

## Success Metrics

- ✅ Service areas section published on contact page
- ✅ Both English and Chinese versions live
- ✅ Track Google Search Console for queries like:
  - "acupuncture burnaby"
  - "tcm coquitlam"
  - "acupuncture surrey near new westminster"
- ✅ Monitor if any traffic from these neighboring cities increases

---

## Timeline

**Estimated Time**: 1-2 hours
- Content creation: 30 min
- Template update: 30 min
- Chinese translation: 30 min
- Testing: 30 min

**Target Completion**: Month 3 (Scaling phase)

---

## Optional Enhancement

Add a simple map showing your location relative to these cities (can be a static image or Google Maps embed with pins for each area).
