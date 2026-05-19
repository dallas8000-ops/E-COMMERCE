function Home() {
  return (
    <div className="text-center">
      <h1>Welcome to East Africa Fashion</h1>
      <small className="text-muted d-block mb-2">Tukusanyukidde mu East Africa Fashion</small>
      <p className="lead">Shop the latest in women's clothing, accessories, jewelry, shoes, rings, perfume, and lingerie. Curated for East Africa, inspired by global trends.</p>
      <small className="text-muted d-block mb-3">Gula ebyambalo ebipya by'abakyala, ebikwasirako, obusaale, engatto, n'ebyobe. Bikozesebwa mu Afurika y'Ebuvanjuba, bikubbibwa okuva mu nsi yonna.</small>
      <img src="/images/hero.jpg" alt="Fashion Hero" className="img-fluid rounded shadow" style={{maxHeight: '400px'}} />
    </div>
  );
}

export default Home;
