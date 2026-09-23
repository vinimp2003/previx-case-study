// Script Manager for Cookie Consent
// This file handles loading and managing third-party scripts based on user consent

import { CookieConfig } from '../config/cookieConfig';

// Global script state
let analyticsLoaded = false;
let marketingLoaded = false;
let functionalLoaded = false;

// Script loading functions
export const loadGoogleAnalytics = (config: CookieConfig) => {
  if (analyticsLoaded || !config.analyticsId) return;

  // Load Google Analytics script
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${config.analyticsId}`;
  document.head.appendChild(script);

  // Initialize gtag
  window.dataLayer = window.dataLayer || [];
  function gtag(...args: unknown[]) {
    window.dataLayer?.push(args);
  }
  window.gtag = gtag;

  gtag('js', new Date());
  gtag('config', config.analyticsId, {
    anonymize_ip: true,
    cookie_flags: 'SameSite=None;Secure',
  });

  analyticsLoaded = true;
  console.log('Google Analytics loaded');
};

export const loadFacebookPixel = (config: CookieConfig) => {
  if (marketingLoaded || !config.facebookPixelId) return;

  // Load Facebook Pixel script
  const script = document.createElement('script');
  script.innerHTML = `
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '${config.facebookPixelId}');
    fbq('track', 'PageView');
  `;
  document.head.appendChild(script);

  marketingLoaded = true;
  console.log('Facebook Pixel loaded');
};

export const loadGoogleAds = (config: CookieConfig) => {
  if (!config.googleAdsId) return;

  // Google Ads is loaded with Google Analytics
  if (window.gtag) {
    window.gtag('config', config.googleAdsId);
    console.log('Google Ads configured');
  }
};

export const loadFunctionalScripts = () => {
  if (functionalLoaded) return;

  // Load any functional scripts here
  // For example: chat widgets, form analytics, etc.
  
  functionalLoaded = true;
  console.log('Functional scripts loaded');
};

// Consent management functions
export const enableAnalytics = (config: CookieConfig) => {
  loadGoogleAnalytics(config);
  
  // Update consent for Google Analytics
  if (window.gtag) {
    window.gtag('consent', 'update', {
      analytics_storage: 'granted',
    });
  }
};

export const enableMarketing = (config: CookieConfig) => {
  loadFacebookPixel(config);
  loadGoogleAds(config);
  
  // Update consent for Facebook Pixel
  if (window.fbq) {
    window.fbq('consent', 'grant');
  }
  
  // Update consent for Google Ads
  if (window.gtag) {
    window.gtag('consent', 'update', {
      ad_storage: 'granted',
    });
  }
};

export const enableFunctional = () => {
  loadFunctionalScripts();
};

export const disableAnalytics = () => {
  // Disable Google Analytics
  if (window.gtag) {
    window.gtag('consent', 'update', {
      analytics_storage: 'denied',
    });
  }
};

export const disableMarketing = () => {
  // Disable Facebook Pixel
  if (window.fbq) {
    window.fbq('consent', 'revoke');
  }
  
  // Disable Google Ads
  if (window.gtag) {
    window.gtag('consent', 'update', {
      ad_storage: 'denied',
    });
  }
};

export const disableFunctional = () => {
  // Disable functional scripts
  console.log('Functional scripts disabled');
};

// Initialize consent mode (required for Google Analytics)
export const initializeConsentMode = () => {
  if (typeof window === 'undefined') return;

  // Set default consent state
  window.gtag = window.gtag || function(...args: unknown[]) {
    (window.dataLayer = window.dataLayer || []).push(args);
  };

  window.gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    functionality_storage: 'denied',
    personalization_storage: 'denied',
    security_storage: 'granted',
  });
};

// Extend Window interface for TypeScript
declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
    fbq?: (...args: unknown[]) => void;
    dataLayer?: unknown[];
  }
}
