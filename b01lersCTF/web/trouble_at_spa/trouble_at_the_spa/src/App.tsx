import Header from './Header.tsx';
import AdCard from './AdCard.tsx';
import Footer from './Footer.tsx';


function App() {
    const sponsors = ['microsoft.svg', 'google.svg', 'amazon.svg', 'netflix.svg', 'meta.svg', 'apple.svg'];

    return (
        <>
            <Header />

            <section className="text-center pt-24">
                <h1 className="text-7xl mb-4 font-bold">
                    Quantum b01lerchain
                </h1>
                <p>
                    Quantum-computing based blockchain technology at scale, automatically secured by cutting-edge
                    AI threat-assessment models.
                </p>
            </section>

            <section className="pt-14 pb-2 mb-20">
                <div className="w-full mx-auto -z-10 bg-gradient-to-r from-yellow-500 via-pink-400 to-red-500 transform -skew-y-3 flex flex-row">
                    <div className="transform skew-y-3 mx-auto -my-4 flex flex-row space-x-12">
                        <AdCard
                            title="Quantum powered"
                            src="/0f5146d5ed9441853c3f2821745a4173.jpg"
                        >
                            Leveraging distributed quantum compute power, b01lerchain technology achieves energy
                            efficiency where other blockchains fail.
                        </AdCard>
                        <AdCard
                            title="Blockchain at scale"
                            src="/0bee89b07a248e27c83fc3d5951213c1.jpg"
                        >
                            All b01lerchain transactions are backed up across 10 different blockchains,
                            ensuring data security.
                        </AdCard>
                        <AdCard
                            title="AI++"
                            src="/5ab557c937e38f15291c04b7e99544ad.jpg"
                        >
                            Leveraging scalable quantum compute power, b01lerchain technology achieves energy efficiency
                            where other blockchains fail.
                        </AdCard>
                    </div>
                </div>
            </section>

            <section className="mb-8">
                <p className="text-sm text-center text-secondary mb-3">
                    Proudly powered by
                </p>
                <div className="flex gap-x-10 gap-y-2 items-center flex-wrap justify-center px-6">
                    {sponsors.map((l) => (
                        <img
                            src={l}
                            className="h-12"
                            key={l}
                        />
                    ))}
                </div>
            </section>

            <h3 className="font-bold text-xl text-center mb-8">
                Join 1,200+ investors sharing in b01lerchain's vision.
            </h3>

            <section>
                <p className="max-w-5xl px-8 mx-auto mb-8">
                    View our demo below:
                </p>
                <img
                    src="/483032a6422b3ba7005dfa12dda874b5.jpg"
                    className="w-full h-[30rem] object-cover object-center opacity-50"
                />
            </section>

            <Footer />
        </>
    )
}

export default App;
