"""
Word lists and patterns for subscription page linguistic analysis.
All lists are lowercase for case-insensitive matching.
"""

# Motivation Framework
SUPPORT_TERMS = [
    'support', 'contribute', 'fund', 'enable', 'help', 'sustain', 
    'back', 'empower', 'donation', 'contribution', 'supporting',
    'contribute to', 'help us', 'support us', 'fund our', 'enable us',
    'sustain our', 'back our', 'empower us', 'your donation', 'your contribution'
]

TRANSACTIONAL_TERMS = [
    'buy', 'purchase', 'subscribe', 'order', 'get', 'start', 
    'sign up', 'register', 'checkout', 'cart', 'payment', 'pay',
    'buying', 'purchasing', 'subscription', 'ordering', 'getting',
    'add to cart', 'proceed to checkout', 'complete order', 'pay now'
]

MISSION_TERMS = [
    'journalism', 'democracy', 'truth', 'independent', 'fearless', 
    'quality', 'investigative', 'reporting', 'accountability', 
    'public interest', 'free press', 'fourth estate', 'watchdog',
    'unbiased', 'integrity', 'transparency', 'fact-based', 'rigorous',
    'in-depth', 'credible', 'trustworthy', 'ethical', 'professional',
    'quality journalism', 'independent journalism', 'investigative reporting',
    'holding power to account', 'speaking truth to power'
]

FEATURE_TERMS = [
    'access', 'content', 'articles', 'digital', 'unlimited', 
    'exclusive', 'ad-free', 'premium', 'archive', 'newsletter',
    'benefits', 'perks', 'features', 'included', 'full access',
    'all articles', 'premium content', 'exclusive content', 'digital access',
    'unlimited reading', 'no ads', 'archive access', 'early access',
    'bonus content', 'special reports', 'subscriber-only'
]

IDENTITY_TERMS = [
    'member', 'supporter', 'reader', 'community', 'partner', 
    'patron', 'backer', 'champion', 'advocate', 'membership',
    'insider', 'subscriber', 'valued member', 'loyal reader',
    'join our community', 'become a member', 'our supporters',
    'reader community', 'partner with us'
]

COMMUNITY_TERMS = [
    'our', 'we', 'us', 'together', 'join', 'fellow', 
    'collective', 'shared', 'common', 'community', 'family',
    'join us', 'we believe', 'our mission', 'together we',
    'collective effort', 'shared values', 'common cause',
    'our readers', 'we need', 'help us', 'with us'
]

# Behavioral Triggers
SCARCITY_TERMS = [
    'limited time', 'ends', 'only', 'exclusive', 'last chance', 
    'today only', 'hurry', 'final', 'remaining', 'expires',
    'ending soon', 'don\'t wait', 'act now', 'while supplies last',
    'limited offer', 'special offer', 'time-limited', 'deadline',
    'ends today', 'ends tomorrow', 'ends this week', 'final days',
    'only available', 'spots remaining', 'seats left'
]

SOCIAL_PROOF_TERMS = [
    'most popular', 'recommended', 'bestseller', 'readers choice', 
    'trusted by', 'joined by', 'chosen by', 'preferred by',
    'thousands of readers', 'millions trust', 'readers love',
    'highly rated', 'top choice', 'award-winning', 'acclaimed',
    'reader favorite', 'highly recommended', 'widely read',
    'growing community', 'join thousands', 'trusted source'
]

# Regex patterns for social proof (e.g., "50,000 subscribers", "1M readers")
SOCIAL_PROOF_PATTERNS = [
    r'\d+[,\d]*\s*(k|K|thousand|Thousand|million|Million|M|m)?\s*(subscribers?|readers?|members?|supporters?|users?)',
    r'(thousands?|millions?|hundreds?)\s+of\s+(subscribers?|readers?|members?|supporters?|users?)',
    r'over\s+\d+[,\d]*\s*(subscribers?|readers?|members?|supporters?|users?)',
    r'\d+[,\d]*\+?\s*(people|individuals|customers)\s+(subscribe|read|support|trust)',
]

LOSS_AVERSION_TERMS = [
    'miss', 'lose', 'don\'t miss out', 'never miss', 'missing out',
    'full access', 'complete', 'everything', 'all', 'entire',
    'without limits', 'no restrictions', 'unrestricted', 'comprehensive',
    'miss out on', 'lose access', 'won\'t have', 'can\'t access',
    'exclusive to subscribers', 'members only', 'subscriber exclusive',
    'all the news', 'complete coverage', 'full story', 'whole picture'
]

RECIPROCITY_TERMS = [
    'support enables', 'your contribution', 'thanks to readers', 
    'rely on', 'made possible', 'because of you', 'your support',
    'reader-funded', 'reader-supported', 'powered by readers',
    'depends on', 'sustained by', 'funded by readers', 'your help',
    'make it possible', 'enable our work', 'support our mission',
    'contribution matters', 'every subscription counts', 'you make',
    'readers like you', 'supporters like you'
]

# Habit Formation
TEMPORAL_ANCHORS = [
    'daily', 'morning', 'evening', 'weekly', 'everyday', 
    'routine', 'breakfast', 'commute', 'lunch break', 'bedtime',
    'each day', 'every morning', 'every evening', 'start your day',
    'end your day', 'morning briefing', 'evening digest', 'weekend',
    'weekday', 'daily dose', 'morning read', 'evening update',
    'coffee break', 'daily habit', 'part of your day'
]

FREQUENCY_TERMS = [
    'always', 'whenever', 'anytime', 'regularly', 'every morning',
    'each day', 'constantly', '24/7', 'round the clock', 'ongoing',
    'continuous', 'never-ending', 'perpetual', 'consistent',
    'reliable', 'dependable', 'always available', 'always there',
    'whenever you want', 'on demand', 'as often as', 'unlimited times'
]

CONVENIENCE_TERMS = [
    'easy', 'simple', 'seamless', 'convenient', 'anywhere',
    'effortless', 'instant', 'quick', 'straightforward', 'hassle-free',
    'one-click', 'user-friendly', 'intuitive', 'smooth', 'frictionless',
    'no hassle', 'easily', 'simply', 'quickly', 'instantly',
    'easy access', 'simple process', 'convenient access', 'quick setup',
    'easy to use', 'simple to start'
]

PLATFORM_TERMS = [
    'app', 'mobile', 'tablet', 'desktop', 'device', 'platform',
    'ios', 'android', 'smartphone', 'computer', 'all your devices',
    'cross-platform', 'multi-device', 'responsive', 'native app',
    'mobile app', 'desktop app', 'web app', 'download the app',
    'available on', 'compatible with', 'works on', 'sync across',
    'access from', 'read on', 'use on any device'
]

# Price-related patterns for additional analysis
PRICE_PATTERNS = [
    r'\$\d+\.?\d*',
    r'\£\d+\.?\d*',
    r'\€\d+\.?\d*',
    r'\d+\.?\d*\s*(dollar|pound|euro|usd|gbp|eur)',
    r'(free|complimentary)\s+(trial|access|month|week|period)',
    r'\d+\s*(day|week|month|year)s?\s+(free|trial|access)',
]