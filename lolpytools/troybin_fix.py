fix_troybin_system = [
    [
        ["System"],
        [
            what %x for x in range(0, 50) for what in
            [
                "GroupPart%d",
                "GroupPart%dImportance",
                "GroupPart%dType",
                "Override-Offset%d",
                "Override-Rotation%d",
                "Override-Scale%d",
            ]
        ] + [
            "AudioFlexValueParameterName",
            "AudioParameterFlexID",
            "Build-Up-Time",
            "Group-Vis",
            "Group-Scale-Cap",
            "KeepOrientationAfterSpellCast",
        ] + fix_material_override + [
            "PersistThruDeath",
            "PersistThruRevive",
            "SelfIllumination",
            "SimulateEveryFrame",
            "SimulateOncePerFrame",
            "SimulateWhileOffScreen",
            "SoundEndsOnEmitterEnd",
            "SoundOnCreate",
            "SoundPersistent",
            "SoundsPlayWhileOffScreen",
            "VoiceOverOnCreate",
            "VoiceOverPersistent",
        ]
    ],
]

fix_troybin_names_vectors = [
        'Emitter-BirthRotationalAcceleration',
        'Particle-Acceleration',
        "Particle-Drag",
        'Particle-Velocity',
        'e-censor-modulate',
        'e-color-modulate',
        'e-ratebyvel',
        'e-framerate',
        'e-rate',
        'e-rate_flex',
        'e-rgba',
    ] + [
        "e-rotation%d" % x for x in range(0, 10)
    ] + [
        'e-tilesize',
        'e-uvoffset',
        'e-uvoffset-mult',
        'e-uvoffset_flex',
        'f-accel',
        'f-direction',
        'f-drag',
        'f-period',
        'f-pos',
        'f-radius',
        'f-veldelta',
        'p-accel',
        'p-bindtoemitter',
        'p-childProb',
        'p-drag',
        'p-fresnel-color',
        'p-life',
        'p-life_flex',
        'p-offset',
        'p-orbitvel',
        'p-postoffset',
        'p-quadrot',
        'p-reflection-fresnel-color',
        'p-rotvel',
        'p-rotvel_flex',
        'p-scale',
        'p-uvscroll-rgb',
        'p-uvscroll-rgb-mult',
        'p-vel',
        'p-worldaccel',
        "p-xquadrot",
        'p-xscale',
        'p-xrgba',
    ]

fix_troybin_names = fix_troybin_names_vectors + [
        'p-skeleton',
        'p-skin',
        'p-vec-velocity-minscale',
        'p-vec-velocity-scale',
    ] + [
        "%s%sP%d" % (n,v,p) for p in range(1, 5) for v in ["X", "Y", "Z"] for n in fix_troybin_names_vectors
    ] + [
        "%sP%d" % (n,p) for p in range(1, 5) for n in fix_troybin_names_vectors
    ] + [
        "%s%d" % (n,p) for p in range(1, 5) for n in fix_troybin_names_vectors
    ] + [
        'KeywordsExcluded',
        'KeywordsRequired',
        'KeywordsIncluded',
        'p-texture-mode',
        'p-texture-mult-mode',
        'wrap',
        'flag-disable-z',
        'flag-force-animated-mesh-z-write',
        'flag-projected',
        'flag-brighter-in-fow',
        'p-backfaceon',
        'p-texture-mult',
        'p-texdiv-mult',
        'p-falloff-texture',
        'p-normal-map',
        'p-reflection-map',
        'p-reflection-opacity-direct',
        'p-reflection-opacity-glancing',
        'p-reflection-fresnel',
        'p-fresnel',
        'default-e-life',
        'e-timeoffset',
        'e-life',
        'e-life-scale',
        'e-active',
        'e-period',
        'e-trail-cutoff',
        'e-beam-segments',
        'single-particle',
        'p-life-scale',
        'p-life-scale-offset',
        'p-life-scale-symX',
        'p-life-scale-symY',
        'p-life-scale-symZ',
        'p-distortion-power',
        'p-distortion-mode',
        'p-alphaslicerange',
        'e-censor-policy',
        'e-framerate',
        'e-local-orient',
        'p-texture-pixelate',
        # TODO: is there anything else using -axis and is there more than 2/3?
    ] + [
        "e-rotation-%d" % x for x in range(0, 10)
    ] + [
        "e-rotation%d-axis" % x for x in range(0, 10)
    ] + [
        'p-colortype',
        'p-colorscale',
        'p-coloroffset',
        'p-linger',
        'e-linger',
        'p-flexoffset',
        'p-flexscale',
        'p-offsetbyheight',
        'p-scalebyheight',
        'p-scalebyheight',
        'p-scalebyradius',
        'p-scaleEmitOffset',
        'e-uvscroll',
        'e-uvscroll-mult',
        'p-trans-sample',
        'fluid-params',
        'submesh-list',
        'p-startframe',
        'p-startframe-mult',
        'p-numframes',
        'p-numframes-mult',
        'p-framerate',
        'p-framerate-mult',
        'p-type',
        'p-mesh',
        'p-meshtex',
        'p-meshtex-mult',
        'e-shape-name',
        'e-shape-scale',
        'e-shape-use-normal-for-birth',
        'p-projection-y-range',
        'p-projection-fading',
        'p-uvscroll-alpha-mult',
        'p-uvscroll-rgb-clamp',
        'p-uvscroll-rgb-clamp-mult',
        'p-xquadrot',
        'p-xquadrot-on',
        'p-vecalign',
        'uniformscale',
        'p-vec-velocity-scale'
        'p-vec-velocity-minscale',
        'p-orientation',
        'p-local-orient',
        'p-randomstartframe',
        'p-randomstartframe-mult',
        'p-shadow',
        'p-uvmode',
        'p-uvscroll-no-alpha',
        'p-uvparallax-scale',
        'p-trailmode',
        'p-beammode',
        'p-followterrain',
        'p-animation',
        'ChildParticleName',
        'ChildEmitOnDeath',
        'ChildSpawnAtBone',
        'f-localspace',
        #TODO: find number here
    ] + [
        what % x for x in range(0, 10) for what in [
            'field-accel-%d',
            'field-attract-%d',
            'field-drag-%d',
            'field-noise-%d',
            'field-orbit-%d',
        ]
    ] + [
        'f-axisfrac',
        'f-viscosity',
        'f-diffusion',
        'f-buoyancy',
        'f-dissipation',
        'f-startkick',
        'f-denseforce',
        'f-movement-x',
        'f-movement-y',
    ] + [
        what % x for x in range(0, 10) for what in [
            'f-jetpos%u',
            'f-jetdir%u',
            'f-jetspeed%u',
            'f-jetdirdiff%u',
        ]
    ] + [
        'f-initdensity',
        'f-life',
        'f-rate',
        'f-rendersize',
        'e-disabled',
        'e-soft-in-depth',
        'e-soft-out-depth',
        'e-soft-in-depth-delta',
        'e-soft-out-depth-delta',
        'Particle-ScaleAlongMovementVector',
        'p-fixedorbit',
        'p-fixedorbittype',
        'p-lockedtoemitter',
        'p-scalebias',
        'p-simpleorient',
        'p-scaleupfromorigin',
        "teamcolor-correction",
        "rendermode",
        "pass",
        "e-alpharef",
        "p-texture",
        "p-texdiv",
        "p-rgba",
    ]



def fix_troybin_sections(tbin):
    fix_inibin(tbin, all_troybin_fixdict)
    if not "System" in tbin["Values"]:
        return []
    system = tbin["Values"]["System"]
    return [ str(system["GroupPart%d" % x]) for x in range(0,50) if "GroupPart%d" % x in system ]

def troybin_fixdict(tbin):
    sections = fix_troybin_sections(tbin)
    return fixarrays2fixdict(sections, fix_troybin_names, None)

def fix_troybin(tbin):
    fix_inibin(tbin, troybin_fixdict(tbin))

