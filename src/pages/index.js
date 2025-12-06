// import clsx from 'clsx';
// import Link from '@docusaurus/Link';
// import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import Layout from '@theme/Layout';
// import HomepageFeatures from '@site/src/components/HomepageFeatures';

// import Heading from '@theme/Heading';
// import styles from './index.module.css';

// function HomepageHeader() {
//   const {siteConfig} = useDocusaurusContext();
//   return (
//     <header className={clsx('hero hero--primary', styles.heroBanner)}>
//       <div className="container">
//         <Heading as="h1" className="hero__title">
//           {siteConfig.title}
//         </Heading>
//         <p className="hero__subtitle">{siteConfig.tagline}</p>
//         <div className={styles.buttons}>
//           <Link
//             className="button button--secondary button--lg"
//             to="/docs/intro">
//             Docusaurus Tutorial - 5min ⏱️
//           </Link>
//         </div>
//       </div>
//     </header>
//   );
// }

// export default function Home() {
//   const {siteConfig} = useDocusaurusContext();
//   return (
//     <Layout
//       title={`Hello from ${siteConfig.title}`}
//       description="Description will go into a meta tag in <head />">
//       <HomepageHeader />
//       <main>
//         <HomepageFeatures />
//       </main>
//     </Layout>
//   );
// }
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

import styles from './index.module.css';

function ModuleCard({ number, title, desc, link, gradient, delay = 0 }) {
    const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.2 });

    return (
        <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 60 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay }}
        >
            <Link to={link} className={styles.moduleCard}>
                <div className={styles.cardGradient} style={{ background: gradient }} />
                <div className={styles.cardContent}>
                    <span className={styles.moduleNumber}>{number}</span>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <span className={styles.cardArrow}>Explore Module →</span>
                </div>
            </Link>
        </motion.div>
    );
}

export default function Home() {
    const { siteConfig } = useDocusaurusContext();

    return (
        <Layout title={siteConfig.title} description={siteConfig.tagline}>
            {/* ==================== HERO SECTION ==================== */}
            <header className={styles.hero}>
                <div className={styles.heroOverlay} />

                {/* Yeh motion.div ab perfectly closed hai */}
                <motion.div
                    className="container"
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1 }}
                >
                    <motion.h1
                        className={styles.heroTitle}
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                    >
                        {siteConfig.title}
                    </motion.h1>

                    <motion.p
                        className={styles.heroSubtitle}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.6 }}
                    >
                        {siteConfig.tagline}
                    </motion.p>

                    <motion.div
                        className={styles.heroButtons}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.9 }}
                    >
                        <Link to="/docs/intro" className="button button--primary button--lg">
                            Start Building Now
                        </Link>
                        <Link
                            to="/docs/hardware/economy-kit"
                            className="button button--outline button--secondary button--lg margin-left--md"
                        >
                            View Hardware Kits →
                        </Link>
                    </motion.div>

                    {/* Stats */}
                    <div className={styles.statsGrid}>
                        <div className={styles.statItem}>
                            <h3>13 Weeks</h3>
                            <p>Zero to Humanoid</p>
                        </div>
                        <div className={styles.statItem}>
                            <h3>4 Modules</h3>
                            <p>Full Stack</p>
                        </div>
                        <div className={styles.statItem}>
                            <h3>100%</h3>
                            <p>Hands-on</p>
                        </div>
                        <div className={styles.statItem}>
                            <h3>2025</h3>
                            <p>Cutting Edge</p>
                        </div>
                    </div>
                </motion.div>
                {/* motion.div closed properly here */}
            </header>

            {/* header closed */}

            <main>
                {/* ==================== MODULES SECTION ==================== */}
                <section className={styles.modulesSection}>
                    <div className="container">
                        <motion.div
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.8 }}
                            className="text--center margin-bottom--xl"
                        >
                            <h2 className={styles.sectionHeading}>
                                The 2025 Robotics Stack You Will Master
                            </h2>
                            <p className="hero__subtitle">From ROS 2 to Vision-Language-Action on real humanoids</p>
                        </motion.div>

                        <div className={styles.modulesGrid}>
                            <ModuleCard
                                number="01"
                                title="ROS 2 Jazzy"
                                desc="The Robotic Nervous System – Real-time, DDS, Lifecycle Nodes"
                                link="/docs/modules/ros2"
                                gradient="linear-gradient(135deg, #00d4ff, #090979)"
                            />
                            <ModuleCard
                                number="02"
                                title="Gazebo + Unity"
                                desc="Photorealistic Simulation & Digital Twins"
                                link="/docs/modules/gazebo-unity"
                                gradient="linear-gradient(135deg, #ff6ec7, #7d2ae8)"
                                delay={0.1}
                            />
                            <ModuleCard
                                number="03"
                                title="NVIDIA Isaac Sim"
                                desc="GPU Physics, Isaac Lab, Foundation Models"
                                link="/docs/modules/nvidia-isaac"
                                gradient="linear-gradient(135deg, #76b900, #000000)"
                                delay={0.2}
                            />
                            <ModuleCard
                                number="04"
                                title="VLA Capstone"
                                desc="Deploy OpenVLA / GR00T on Real Humanoid"
                                link="/docs/modules/vla-capstone"
                                gradient="linear-gradient(135deg, #ff9d00, #ff2e63)"
                                delay={0.3}
                            />
                        </div>
                    </div>
                </section>

                {/* ==================== FINAL CTA ==================== */}
                <section className={styles.ctaFinal}>
                    <motion.div
                        className="container text--center padding-vert--xl"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        transition={{ duration: 1 }}
                    >
                        <h2 className={styles.ctaTitle}>The Future Is Autonomous</h2>
                        <p className={styles.ctaSubtitle}>
                            In just <strong>13 weeks</strong>, you’ll go from zero to deploying a{' '}
                            <strong>Vision-Language-Action powered humanoid robot</strong> using the same stack as{' '}
                            <strong>Tesla Optimus, Figure, Boston Dynamics, 1X</strong> in 2025.
                        </p>
                        <Link
                            to="/docs/intro"
                            className="button button--primary button--lg margin-top--lg"
                        >
                            Start Your Journey Today →
                        </Link>
                    </motion.div>
                </section>
            </main>
        </Layout>
    );
}