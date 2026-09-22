// ─────────────────────────────────────────────────────────────
//  THIS IS THE ONLY FILE YOU NEED TO EDIT.
//
//  To release a chapter:
//    1. Put its mp3 in the "audio" folder, named like the `file` line below.
//    2. Change that chapter's  status: "soon"  to  status: "ready".
//    3. Commit and push. The page does the rest (bees, glow, "up next").
//
//  To tease a chapter, set  soonText: "Coming Saturday!"  (or leave it "").
// ─────────────────────────────────────────────────────────────

window.STORYBOOK = {
  dedication: {
    forNames: "Mia, Theo & June",
    fromLine: "with love from",
    fromName: "Uncle Grant",
    // Optional extra line under the names, like the small print in a book. Leave "" for none.
    message: "",
  },

  welcome: {
    title: "A note from Uncle Grant",
    subtitle: "Listen to this one first",
    file: "audio/00-welcome.mp3",
    picture: "art/welcome.png",
    wash: "#F1DDAE",
    // Hidden until it's recorded. Change to "ready" once audio/00-welcome.mp3 exists.
    status: "soon",
  },

  chapters: [
    {
      number: 1,
      short: "Pooh and Some Bees",
      title: "In Which We Are Introduced to Winnie-the-Pooh and Some Bees, and the Stories Begin",
      picture: "art/ch1.png",
      wash: "#B8D0E0",
      file: "audio/01-pooh-and-some-bees.mp3",
      minutes: 15,
      status: "ready",
      soonText: "",
    },
    {
      number: 2,
      short: "Pooh Gets Stuck",
      title: "In Which Pooh Goes Visiting and Gets into a Tight Place",
      picture: "art/ch2.png",
      wash: "#B9C9A0",
      file: "audio/02-pooh-gets-stuck.mp3",
      status: "soon",
      soonText: "",
    },
    {
      number: 3,
      short: "The Woozle Hunt",
      title: "In Which Pooh and Piglet Go Hunting and Nearly Catch a Woozle",
      picture: "art/ch3.png",
      wash: "#DCE6EC",
      file: "audio/03-the-woozle-hunt.mp3",
      status: "soon",
      soonText: "",
    },
    {
      number: 4,
      short: "Eeyore's Tail",
      title: "In Which Eeyore Loses a Tail and Pooh Finds One",
      picture: "art/ch4.png",
      wash: "#E7C3BC",
      file: "audio/04-eeyores-tail.mp3",
      status: "soon",
      soonText: "",
    },
    {
      number: 5,
      short: "The Heffalump",
      title: "In Which Piglet Meets a Heffalump",
      picture: "art/ch5.png",
      wash: "#F1D089",
      file: "audio/05-the-heffalump.mp3",
      status: "soon",
      soonText: "",
    },
    {
      number: 6,
      short: "Eeyore's Birthday",
      title: "In Which Eeyore Has a Birthday and Gets Two Presents",
      picture: "art/ch6.png",
      wash: "#E7B8B0",
      file: "audio/06-eeyores-birthday.mp3",
      status: "soon",
      soonText: "",
    },
    {
      number: 7,
      short: "Kanga and Baby Roo",
      title: "In Which Kanga and Baby Roo Come to the Forest, and Piglet Has a Bath",
      picture: "art/ch7.png",
      wash: "#C5D3AE",
      file: "audio/07-kanga-and-baby-roo.mp3",
      status: "soon",
      soonText: "",
    },
    {
      number: 8,
      short: "The Expotition",
      title: "In Which Christopher Robin Leads an Expotition to the North Pole",
      picture: "art/ch8.png",
      wash: "#C9DCE6",
      file: "audio/08-the-expotition.mp3",
      status: "soon",
      soonText: "",
    },
    {
      number: 9,
      short: "Piglet and the Flood",
      title: "In Which Piglet Is Entirely Surrounded by Water",
      picture: "art/ch9.png",
      wash: "#AFC8D8",
      file: "audio/09-piglet-and-the-flood.mp3",
      status: "soon",
      soonText: "",
    },
    {
      number: 10,
      short: "Pooh's Party",
      title: "In Which Christopher Robin Gives Pooh a Party, and We Say Goodbye",
      picture: "art/ch10.png",
      wash: "#F1D089",
      file: "audio/10-poohs-party.mp3",
      status: "soon",
      soonText: "",
    },
  ],
};
