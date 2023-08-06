describe("TermCastPlayer", function() {
  var player;
  var song;

  beforeEach(function() {
      player = 'foo';
    // player = new Player();
    // song = new Song();
  });

  it("should have global vars loaded", function() {
    //player.play(song);
    expect(window.TermCast).not.toBeUndefined();
    expect(TC).not.toBeUndefined();
    expect(TC.stream).not.toBeUndefined();
    expect(TC.setup_termcast_tag).not.toBeUndefined();
    expect(TC.all_casts).not.toBeUndefined();
    ////demonstrates use of custom matcher
    //expect(player).toBePlaying(song);
  });
});
