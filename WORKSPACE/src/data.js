// Static demo data for the layout. Each conversation has a few messages
// so the interface looks realistic on first load.

export const conversations = [
  {
    id: 'icona-lives-website-bot',
    name: 'Icona Lives Website Bot',
    preview: "Got it. Everything live stays fr…",
    messages: [
      { from: 'user', text: "don't match their pre-change hashes. Both were changed at 12:44 PM with your 12:42 approval, and the backup copies differ, as expected." },
      { from: 'user', text: 'Nothing live has changed since 12:44, and scripts/chat-responder.py is unchanged since 10:33 AM. So the label fix and the card cleanup are now active.' },
      { from: 'bot', text: 'Thanks — that clears up the live state. Current state accepted: live has only the label fix and card cleanup; responder PID 47461 restarted at 1:14:33; card 180e is untouched.' },
      { from: 'bot', text: 'Keep all live actions frozen. Do not tap card 180e, send test requests, restart again, or roll back unless I approve after review.' },
      { from: 'user', text: "Got it. Everything live stays frozen, and the corrected report will include the live-state timeline with proof alongside the 12 staging and isolation items." },
    ],
  },
  {
    id: 'socials-bot',
    name: 'Socials Bot',
    preview: 'Billionaire mentor and Jordan …',
    messages: [
      { from: 'user', text: 'Can you queue tonight’s posts?' },
      { from: 'bot', text: 'Billionaire mentor and Jordan the Outreach Bot threads are drafted. Ready for your review.' },
    ],
  },
  {
    id: 'icona-live-assistant',
    name: 'Icona Live Assistant',
    preview: 'I fixed the names on both of…',
    messages: [
      { from: 'user', text: 'The names still look wrong.' },
      { from: 'bot', text: 'I fixed the names on both of the live cards. They should now match the roster.' },
    ],
  },
  {
    id: 'jordan-outreach',
    name: 'Jordan the Outreach Bot',
    preview: 'Someone liked a comment…',
    messages: [
      { from: 'bot', text: 'Someone liked a comment on your last outreach post. Want me to reply?' },
    ],
  },
  {
    id: 'ebay-bot',
    name: 'Ebay bot • Handles eBay re…',
    preview: 'The "Partially refunded" label…',
    messages: [
      { from: 'bot', text: 'The "Partially refunded" label was applied to three orders. Reviewing them now.' },
    ],
  },
  {
    id: 'pip',
    name: 'Pip',
    preview: "Dani's email is ready to send f…",
    messages: [
      { from: 'bot', text: "Dani's email is ready to send for your approval." },
    ],
  },
  {
    id: 'finance-bot',
    name: 'Finance Bot',
    preview: "Tesla's deadline is today. T…",
    messages: [
      { from: 'bot', text: "Tesla's deadline is today. The payment needs to go out before 5 PM." },
    ],
  },
  {
    id: 'billionaire-mentor',
    name: 'Billionaire mentor',
    preview: 'Tuxedo is at $439.84 net for t…',
    messages: [
      { from: 'bot', text: 'Tuxedo is at $439.84 net for the week. Want the full breakdown?' },
    ],
  },
  {
    id: 'icona-how-to',
    name: 'Icona How-To Clips',
    preview: "This week's video is ready. It's…",
    messages: [
      { from: 'bot', text: "This week's video is ready. It's queued for review." },
    ],
  },
  {
    id: 'therapist',
    name: 'Therapist',
    preview: "Hi Michael, it's time for We…",
    messages: [
      { from: 'bot', text: "Hi Michael, it's time for your weekly check-in. How have you been?" },
    ],
  },
  {
    id: 'ads-research',
    name: 'Ads Research Manager',
    preview: 'I sent Oracle a short write-up…',
    messages: [
      { from: 'bot', text: 'I sent Oracle a short write-up of the ad tests from this week.' },
    ],
  },
  {
    id: 'icona-growth',
    name: 'Icona Growth',
    preview: 'Sellers are slow this week, Mi…',
    messages: [
      { from: 'bot', text: 'Sellers are slow this week, Michael. I pulled a few ideas to help.' },
    ],
  },
  {
    id: 'michael-lynch',
    name: 'Michael Lynch',
    preview: '87',
    messages: [
      { from: 'bot', text: 'You have 87 unread items across your bots.' },
    ],
  },
]
