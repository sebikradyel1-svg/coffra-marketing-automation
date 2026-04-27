# Coffra Schema Markup Implementation Guide

**Project:** P4 · Coffra Answer Engine Optimization
**Author:** Sebastian Kradyel
**Date:** April 2026
**Document:** docs/12_schema_implementation.md

---

## Purpose

This document provides copy-paste-ready Schema.org markup for every Coffra page type. Schema markup is the structured-data foundation that allows AI engines (ChatGPT, Perplexity, Gemini, Copilot, Claude) and search engines to parse content unambiguously.

Each schema is provided as JSON-LD (the format Google and most AI engines prefer) embedded in `<script type="application/ld+json">` tags. To deploy, paste the relevant block into the `<head>` section of the corresponding page, replacing placeholders with real data.

**Validation:** After deployment, validate every page using:
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org/

Target: zero validation errors across all pages.

---

## 1. Homepage — `Organization` Schema

This is the **most important schema for AEO**. It establishes Coffra as a recognized entity that AI engines build their knowledge graph around.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://coffra.ro/#organization",
  "name": "Coffra",
  "alternateName": "Coffra Specialty Coffee",
  "url": "https://coffra.ro",
  "logo": {
    "@type": "ImageObject",
    "url": "https://coffra.ro/assets/coffra-logo.png",
    "width": 600,
    "height": 600
  },
  "image": "https://coffra.ro/assets/coffra-storefront.jpg",
  "description": "Coffra is a specialty coffee roaster and café founded in Timișoara, Romania in 2026. Coffra sources single-origin beans from farms at 1,800-2,200m altitude, roasts in small batches, and operates a flagship café plus a D2C subscription service.",
  "foundingDate": "2026-01-15",
  "founder": {
    "@type": "Person",
    "@id": "https://coffra.ro/about/sebastian-kradyel#person",
    "name": "Sebastian Kradyel"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Strada Alba Iulia 1",
    "addressLocality": "Timișoara",
    "postalCode": "300077",
    "addressRegion": "Timiș",
    "addressCountry": "RO"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 45.7489,
    "longitude": 21.2087
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+40-256-XXX-XXX",
    "contactType": "customer service",
    "email": "hello@coffra.ro",
    "availableLanguage": ["Romanian", "English"]
  },
  "sameAs": [
    "https://www.instagram.com/coffra.coffee",
    "https://www.linkedin.com/company/coffra",
    "https://www.facebook.com/coffra"
  ],
  "knowsAbout": [
    "Specialty coffee",
    "Single-origin coffee",
    "Coffee roasting",
    "V60 brewing",
    "Espresso",
    "Coffee subscriptions",
    "Romanian craft beverages"
  ],
  "areaServed": {
    "@type": "Country",
    "name": "Romania"
  }
}
</script>
```

**Why this matters:** When ChatGPT is asked "What is Coffra?", the AI uses this schema to construct a factual answer. Without this schema, the AI guesses or omits Coffra entirely.

---

## 2. Café Locations — `LocalBusiness` Schema

Apply to each café location page. Coffra Timișoara is the flagship.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CafeOrCoffeeShop",
  "@id": "https://coffra.ro/locations/timisoara#location",
  "name": "Coffra Timișoara",
  "image": "https://coffra.ro/assets/timisoara-cafe.jpg",
  "telephone": "+40-256-XXX-XXX",
  "email": "timisoara@coffra.ro",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Strada Alba Iulia 1",
    "addressLocality": "Timișoara",
    "postalCode": "300077",
    "addressCountry": "RO"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 45.7489,
    "longitude": 21.2087
  },
  "url": "https://coffra.ro/locations/timisoara",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:30",
      "closes": "20:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday", "Sunday"],
      "opens": "09:00",
      "closes": "18:00"
    }
  ],
  "priceRange": "$$",
  "servesCuisine": "Coffee",
  "menu": "https://coffra.ro/locations/timisoara/menu",
  "acceptsReservations": "False",
  "paymentAccepted": "Cash, Credit Card, Debit Card, Apple Pay, Google Pay",
  "currenciesAccepted": "RON, EUR",
  "hasMap": "https://maps.google.com/?cid=XXXXXX",
  "parentOrganization": {
    "@id": "https://coffra.ro/#organization"
  }
}
</script>
```

---

## 3. Founder/Author Page — `Person` Schema

Apply to Sebastian's bio page. Critical for E-E-A-T signals.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://coffra.ro/about/sebastian-kradyel#person",
  "name": "Sebastian Kradyel",
  "alternateName": "Paul Sebastian Kradyel",
  "image": "https://coffra.ro/assets/sebastian-kradyel.jpg",
  "url": "https://coffra.ro/about/sebastian-kradyel",
  "jobTitle": "Founder and Roaster",
  "worksFor": {
    "@id": "https://coffra.ro/#organization"
  },
  "alumniOf": {
    "@type": "EducationalOrganization",
    "name": "Babeș-Bolyai University",
    "url": "https://www.ubbcluj.ro/"
  },
  "knowsAbout": [
    "Specialty coffee",
    "Coffee roasting",
    "Marketing automation",
    "Customer segmentation",
    "AI marketing"
  ],
  "sameAs": [
    "https://www.linkedin.com/in/sebastian-kradyel",
    "https://github.com/sebikradyel1-svg"
  ],
  "description": "Sebastian Kradyel is the founder and head roaster of Coffra, a specialty coffee company in Timișoara, Romania. He holds a Master's degree in Marketing from Babeș-Bolyai University and combines technical marketing expertise with hands-on coffee roasting experience."
}
</script>
```

---

## 4. Product Pages — `Product` Schema

Apply to every coffee product page. Each origin gets its own schema.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://coffra.ro/products/ethiopia-gelana-250g#product",
  "name": "Ethiopia Gelana Abaya — Single Origin Specialty Coffee",
  "image": [
    "https://coffra.ro/assets/products/ethiopia-gelana-1x1.jpg",
    "https://coffra.ro/assets/products/ethiopia-gelana-4x3.jpg",
    "https://coffra.ro/assets/products/ethiopia-gelana-16x9.jpg"
  ],
  "description": "Ethiopia Gelana Abaya is a naturally-processed specialty coffee from the Sidama region of Ethiopia, sourced from farms at 1,850 meters altitude. Tasting notes: blueberry, dark chocolate, jasmine. Roasted to medium-light for filter brewing methods.",
  "brand": {
    "@id": "https://coffra.ro/#organization"
  },
  "manufacturer": {
    "@id": "https://coffra.ro/#organization"
  },
  "category": "Coffee Beans",
  "sku": "ETH-GEL-250",
  "gtin": "5901234567890",
  "offers": {
    "@type": "Offer",
    "url": "https://coffra.ro/products/ethiopia-gelana-250g",
    "priceCurrency": "RON",
    "price": "120.00",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@id": "https://coffra.ro/#organization"
    },
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {
        "@type": "MonetaryAmount",
        "value": "20.00",
        "currency": "RON"
      },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "businessDays": {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        },
        "cutoffTime": "14:00:00",
        "handlingTime": {
          "@type": "QuantitativeValue",
          "minValue": 1,
          "maxValue": 2,
          "unitCode": "DAY"
        },
        "transitTime": {
          "@type": "QuantitativeValue",
          "minValue": 2,
          "maxValue": 5,
          "unitCode": "DAY"
        }
      }
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "47",
    "bestRating": "5",
    "worstRating": "1"
  },
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "Origin",
      "value": "Sidama, Ethiopia"
    },
    {
      "@type": "PropertyValue",
      "name": "Altitude",
      "value": "1,850 meters"
    },
    {
      "@type": "PropertyValue",
      "name": "Process",
      "value": "Natural"
    },
    {
      "@type": "PropertyValue",
      "name": "Variety",
      "value": "Heirloom"
    },
    {
      "@type": "PropertyValue",
      "name": "Roast Level",
      "value": "Medium-Light"
    },
    {
      "@type": "PropertyValue",
      "name": "Recommended Brew",
      "value": "V60, Aeropress, Drip"
    },
    {
      "@type": "PropertyValue",
      "name": "Tasting Notes",
      "value": "Blueberry, Dark Chocolate, Jasmine"
    },
    {
      "@type": "PropertyValue",
      "name": "Net Weight",
      "value": "250g"
    },
    {
      "@type": "PropertyValue",
      "name": "Roast Date",
      "value": "Within 7 days of order"
    }
  ]
}
</script>
```

**Why detailed `additionalProperty`:** When a Connoisseur asks Perplexity "what's a good naturally-processed Ethiopian coffee under 130 RON?", the AI uses these property values to filter and recommend. Without them, Coffra's product is invisible to such queries.

---

## 5. Coffra Pass Subscription — `Service` Schema

Apply to the Coffra Pass subscription page.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://coffra.ro/coffra-pass#service",
  "name": "Coffra Pass — Monthly Coffee Subscription",
  "description": "Coffra Pass is a monthly subscription that gives members access to 15 cafés at any Coffra location for 245 RON per month. The subscription includes filter coffee, espresso drinks, and seasonal specials. Members can use their cafés flexibly throughout the month with no rollover or cancellation fees.",
  "provider": {
    "@id": "https://coffra.ro/#organization"
  },
  "serviceType": "Coffee Subscription",
  "offers": {
    "@type": "Offer",
    "price": "245.00",
    "priceCurrency": "RON",
    "priceSpecification": {
      "@type": "UnitPriceSpecification",
      "price": "245.00",
      "priceCurrency": "RON",
      "unitCode": "MON",
      "unitText": "month"
    },
    "availability": "https://schema.org/InStock",
    "url": "https://coffra.ro/coffra-pass"
  },
  "areaServed": {
    "@type": "City",
    "name": "Timișoara"
  },
  "termsOfService": "https://coffra.ro/coffra-pass/terms",
  "audience": {
    "@type": "Audience",
    "name": "Daily coffee drinkers and specialty coffee enthusiasts"
  }
}
</script>
```

---

## 6. FAQ Sections — `FAQPage` Schema

The single highest-leverage schema for AEO. Apply to: Coffra Pass page, subscription page, sourcing page, brewing guides, and individual product pages where applicable.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": "https://coffra.ro/coffra-pass#faq",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Coffra Pass?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Coffra Pass is a monthly subscription giving members 15 cafés at any Coffra location for 245 RON. It includes filter coffee, espresso drinks, and seasonal specials, with no cancellation fees and no rollover of unused cafés."
      }
    },
    {
      "@type": "Question",
      "name": "How does Coffra source its coffee?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Coffra sources single-origin specialty coffee from farms at 1,800-2,200 meters altitude across Ethiopia, Colombia, and Kenya. Each lot is cupped before purchase, with approximately 4 of 7 lots typically rejected for not meeting Coffra's quality standards on moisture consistency, processing, and cup score."
      }
    },
    {
      "@type": "Question",
      "name": "How fresh is Coffra coffee?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Coffra roasts in small batches and ships within 7 days of roasting. Roast date is printed on every bag. For optimal flavor, we recommend brewing within 4 weeks of the roast date for filter coffee, or within 6 weeks for espresso."
      }
    },
    {
      "@type": "Question",
      "name": "Can I cancel my Coffra Pass anytime?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Coffra Pass is a month-to-month subscription with no minimum commitment. You can cancel anytime through your account dashboard, and cancellation takes effect at the end of your current billing period."
      }
    },
    {
      "@type": "Question",
      "name": "What's the difference between Coffra and other Romanian coffee brands?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Coffra focuses exclusively on specialty coffee with rigorous sourcing transparency. Each lot is published with origin farm name, altitude, processing method, and cup score. Coffra also offers brewing education through detailed guides and an in-person training program at the Timișoara location, which is uncommon among Romanian coffee brands."
      }
    },
    {
      "@type": "Question",
      "name": "Does Coffra ship internationally?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Coffra currently ships to Romania, Hungary, Bulgaria, Serbia, and Moldova. International shipping rates start at 20 RON for Romania domestic and increase based on destination. Delivery times are 2-5 business days domestic and 5-10 business days for international destinations."
      }
    },
    {
      "@type": "Question",
      "name": "What brewing equipment does Coffra recommend for beginners?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "For beginners, Coffra recommends a Hario V60 with paper filters, a digital scale that measures to 0.1g, and a kettle with a gooseneck spout. The total starting investment is approximately 200-300 RON. Coffra publishes detailed V60 brewing guides at coffra.ro/brewing-guides for learning the technique."
      }
    }
  ]
}
</script>
```

**Why FAQ schema is high-leverage:** AI engines often quote FAQ answers verbatim when responding to user queries. A well-written FAQ effectively becomes the AI engine's answer.

---

## 7. Blog Posts — `Article` + `Author` Schema

Apply to every blog post or content page.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "https://coffra.ro/blog/v60-brewing-guide#article",
  "headline": "How to Brew the Perfect V60: Coffra's Complete Step-by-Step Guide",
  "description": "A complete V60 brewing guide for specialty coffee enthusiasts. Covers grind size, water temperature, pour technique, and troubleshooting common problems.",
  "image": [
    "https://coffra.ro/assets/blog/v60-brewing-1x1.jpg",
    "https://coffra.ro/assets/blog/v60-brewing-4x3.jpg",
    "https://coffra.ro/assets/blog/v60-brewing-16x9.jpg"
  ],
  "datePublished": "2026-04-15T08:00:00+02:00",
  "dateModified": "2026-04-25T14:30:00+02:00",
  "author": {
    "@type": "Person",
    "@id": "https://coffra.ro/about/sebastian-kradyel#person",
    "name": "Sebastian Kradyel",
    "url": "https://coffra.ro/about/sebastian-kradyel"
  },
  "publisher": {
    "@id": "https://coffra.ro/#organization"
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://coffra.ro/blog/v60-brewing-guide"
  },
  "keywords": "V60, pour-over, brewing guide, specialty coffee, Hario, filter coffee",
  "articleSection": "Brewing Guides",
  "wordCount": 2400,
  "inLanguage": "en-US"
}
</script>
```

**Note on `dateModified`:** Update this every time the article is revised. AI engines (especially Perplexity) heavily privilege fresh content.

---

## 8. Brewing Guides — `Recipe` Schema

For brewing guide pages, layer `Recipe` schema on top of `Article` for additional structured signal.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "name": "V60 Pour-Over Brewing Method",
  "image": "https://coffra.ro/assets/recipes/v60-method.jpg",
  "author": {
    "@id": "https://coffra.ro/about/sebastian-kradyel#person"
  },
  "datePublished": "2026-04-15",
  "description": "A precise V60 pour-over brewing method using a 1:16 coffee-to-water ratio for clean, bright extraction of single-origin specialty coffee.",
  "recipeCategory": "Beverage",
  "recipeCuisine": "Coffee",
  "totalTime": "PT4M",
  "recipeYield": "1 cup (250ml)",
  "recipeIngredient": [
    "15g freshly-roasted specialty coffee, ground medium-fine",
    "240g water at 94°C (filtered, low TDS)",
    "1 Hario V60 paper filter"
  ],
  "recipeInstructions": [
    {
      "@type": "HowToStep",
      "name": "Pre-wet filter",
      "text": "Place V60 on top of carafe. Insert paper filter and pre-wet with hot water to remove paper taste. Discard rinse water."
    },
    {
      "@type": "HowToStep",
      "name": "Add coffee",
      "text": "Add 15g of medium-fine ground coffee. Tap to level the bed."
    },
    {
      "@type": "HowToStep",
      "name": "Bloom pour",
      "text": "Start timer. Pour 30g of water in slow circles to saturate all grounds. Wait 30 seconds for the bloom."
    },
    {
      "@type": "HowToStep",
      "name": "Main pours",
      "text": "Pour to 120g total at 0:30. Pour to 200g at 1:15. Pour to 240g at 2:00. Maintain steady, slow circular pours."
    },
    {
      "@type": "HowToStep",
      "name": "Drawdown",
      "text": "Total brew time should be 3:30-4:00. If too fast, grind finer. If too slow, grind coarser."
    }
  ],
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": "5 kcal",
    "servingSize": "250ml"
  }
}
</script>
```

---

## 9. Customer Reviews — `Review` Schema

Embed reviews on product pages. Use `aggregateRating` on `Product` schema and individual `Review` for prominent testimonials.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "Product",
    "@id": "https://coffra.ro/products/ethiopia-gelana-250g#product",
    "name": "Ethiopia Gelana Abaya"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5"
  },
  "author": {
    "@type": "Person",
    "name": "Andrei Popescu"
  },
  "datePublished": "2026-04-10",
  "reviewBody": "The Gelana Abaya is exactly what I look for in a natural Ethiopia — bright blueberry up front, dark chocolate finish. Roast date was 4 days before delivery. This is the standard I wish more Romanian roasters would meet."
}
</script>
```

---

## 10. Events — `Event` Schema

For cupping events, brewing classes, and community gatherings at the Timișoara café.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Coffra Cupping Session — Ethiopia Origins",
  "description": "Free monthly cupping session exploring three Ethiopia single-origin coffees. Learn cupping methodology, taste flavor differences between regions, and discuss with Sebastian and the Coffra team.",
  "startDate": "2026-05-12T18:00:00+03:00",
  "endDate": "2026-05-12T20:00:00+03:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Coffra Timișoara",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Strada Alba Iulia 1",
      "addressLocality": "Timișoara",
      "postalCode": "300077",
      "addressCountry": "RO"
    }
  },
  "image": "https://coffra.ro/assets/events/cupping-ethiopia.jpg",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "RON",
    "url": "https://coffra.ro/events/cupping-ethiopia-may-2026",
    "availability": "https://schema.org/InStock",
    "validFrom": "2026-04-26T00:00:00+03:00"
  },
  "organizer": {
    "@id": "https://coffra.ro/#organization"
  },
  "performer": {
    "@id": "https://coffra.ro/about/sebastian-kradyel#person"
  }
}
</script>
```

---

## 11. Multi-Language — `inLanguage` Annotation

For pages available in both Romanian and English, indicate language and link variants. Apply on `Article`, `WebPage`, etc.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "inLanguage": "ro-RO",
  "translationOfWork": {
    "@type": "Article",
    "@id": "https://coffra.ro/en/blog/v60-brewing-guide#article",
    "inLanguage": "en-US"
  }
}
</script>
```

Also add `<link rel="alternate" hreflang="..." href="...">` tags in HTML `<head>`:

```html
<link rel="alternate" hreflang="ro-RO" href="https://coffra.ro/blog/ghid-v60" />
<link rel="alternate" hreflang="en-US" href="https://coffra.ro/en/blog/v60-brewing-guide" />
<link rel="alternate" hreflang="x-default" href="https://coffra.ro/en/blog/v60-brewing-guide" />
```

This is critical for Romanian-language SEO/AEO competitive advantage — most Romanian coffee brands skip this, leaving Coffra room to dominate local AI queries.

---

## 12. BreadcrumbList — Navigation Context

Apply on every page below the homepage. Helps AI engines understand site structure.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://coffra.ro/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Products",
      "item": "https://coffra.ro/products"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Single Origin",
      "item": "https://coffra.ro/products/single-origin"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "Ethiopia Gelana Abaya",
      "item": "https://coffra.ro/products/ethiopia-gelana-250g"
    }
  ]
}
</script>
```

---

## 13. Implementation Priorities

Deploy schemas in this order based on AEO impact:

| Priority | Schema | Rationale |
|---|---|---|
| 1 | `Organization` (homepage) | Foundation entity for AI knowledge graph |
| 2 | `Person` (founder bio) | E-E-A-T signal |
| 3 | `LocalBusiness` (cafés) | Local search dominance |
| 4 | `Product` (all coffee products) | Direct sales impact |
| 5 | `FAQPage` (key pages) | Highest AEO citation rate |
| 6 | `Article` (blog posts) | Sustained content authority |
| 7 | `Recipe` (brewing guides) | Niche traffic capture |
| 8 | `Service` (Coffra Pass) | Subscription positioning |
| 9 | `Review` (testimonials) | Trust signal |
| 10 | `Event` (cupping sessions) | Community engagement |
| 11 | `BreadcrumbList` (everywhere) | Navigation clarity |
| 12 | `inLanguage` annotations | Bilingual advantage |

---

## 14. Validation Checklist

Before considering AEO setup complete, verify:

- [ ] Every page validates with zero errors via Google Rich Results Test.
- [ ] Every schema has a unique `@id` URI for entity disambiguation.
- [ ] `Organization` schema is consistent across every page (use `@id` references).
- [ ] All URLs in schemas use HTTPS.
- [ ] All dates use ISO 8601 format with timezone.
- [ ] All prices include currency code.
- [ ] All images include width and height where possible.
- [ ] `dateModified` is updated whenever content changes.
- [ ] `aggregateRating` only present when there are real reviews.
- [ ] No schemas reference URLs that 404.

---

## 15. Maintenance Cadence

| Frequency | Action |
|---|---|
| **Daily** | Validate schemas on any new page before publishing |
| **Weekly** | Update `dateModified` on any content that was revised |
| **Monthly** | Re-run all pages through Rich Results Test to catch regressions |
| **Quarterly** | Audit `Organization` schema for any business detail changes |
| **Annually** | Review against Schema.org updates and emerging types |

---

## 16. Tools and Resources

- **Schema.org official:** https://schema.org/ (canonical reference)
- **Google Rich Results Test:** https://search.google.com/test/rich-results
- **Schema.org Validator:** https://validator.schema.org/
- **HubSpot AEO Search Grader:** https://www.hubspot.com/grader (free benchmarking)
- **Google's structured data guidelines:** https://developers.google.com/search/docs/appearance/structured-data

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **April 26, 2026** | Initial schema implementation guide. 12 schema types covering all Coffra page types with copy-paste-ready JSON-LD. Validated against Schema.org spec. |
