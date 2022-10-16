#!/usr/bin/env python
from sys import stderr
RAND_VARS=10
GPART_VARS=50
ROT_VARS=10
FIELD_VARS=10
COMMENTS=("%s", "'%s")

def ihash(value, ret = 0):
    for c in value:
        ret = (ord(c.lower()) + ((65599 * ret) & 0xffffffff)) & 0xffffffff
    return ret

def a_ihash(sections, names):
    for section in sections:
        sectionhash = ihash('*', ihash(section))
        for rawname in names:
            for com in COMMENTS:
                name = com % rawname
                ret = ihash(name, sectionhash)
                yield section, name, ret

def flex(*args):
    return [
        *[ "%s" % a for a in args ],
        *[ "%s_flex" % a for a in args ],
        *[ "%s_flex%d" % (a, x) for a in args for x in range(0,4) ],
    ]

def rand(mods, *args):
    return [
        *args,
        *[ "%s%u" % (a,x) for a in args for x in range(0, RAND_VARS) ],
        *[ "%s%sP" % (a,m) for a in args for m in mods ],
        *[ "%s%sP%u" % (a,m,x) for a in args for m in mods \
            for x in range(0, RAND_VARS)
        ],
    ]

def flex_float(*args):
    return [
        *[ "%s" % a for a in args ],
        *[ "%s_flex" % a for a in args ],
        *[ "%s_flex%d" % (a, x) for a in args for x in range(0,4) ],
    ]

def rand_float(*args):
    return rand(['X', ''], *args)

def rand_vec2(*args):
    return rand(['X', 'Y'], *args)

def rand_vec3(*args):
    return rand(['X', 'Y', 'Z'], *args)

def rand_color(*args):
    return rand(['R', 'G', 'B', 'A'], *args)

def flex_rand_float(*args):
    return rand_float(*flex(*args))

def flex_rand_vec2(*args):
    return rand_vec2(*flex(*args))

def flex_rand_vec3(*args):
    return rand_vec3(*flex(*args))

def flex_rand_color(*args):
    return rand_color(*flex(*args))

material_names = [
    "MaterialOverrideTransMap",
    "MaterialOverrideTransSource",
    "p-trans-sample",
    *[ mat % x for mat in [
        "MaterialOverride%dBlendMode",
        "MaterialOverride%dGlossTexture",
        "MaterialOverride%dEmissiveTexture",
        "MaterialOverride%dFixedAlphaScrolling",
        "MaterialOverride%dPriority",
        "MaterialOverride%dRenderingMode",
        "MaterialOverride%dSubMesh",
        "MaterialOverride%dTexture",
        "MaterialOverride%dUVScroll",
        ] for x in range(0,5) 
    ],
]

part_group_names = [
    *[ "GroupPart%d" % x for x in range(0, GPART_VARS) ],
]

part_field_names = [
    *[ field % x for field in [
            "field-accel-%d",
            "field-attract-%d",
            "field-drag-%d",
            "field-noise-%d",
            "field-orbit-%d",
        ] for x in range(1, FIELD_VARS)
    ],
]

part_fluid_names = [
    "fluid-params",
]

system_names = [
    "AudioFlexValueParameterName",
    "AudioParameterFlexID",
    "build-up-time",
    "group-vis",
    "group-scale-cap",
    *[ g % x for g in [
        "GroupPart%d",
        "GroupPart%dType",
        "GroupPart%dImportance",
        "Override-Offset%d",
        "Override-Rotation%d",
        "Override-Scale%d",
        ] for x in range(0, GPART_VARS)
    ],
    "KeepOrientationAfterSpellCast",
    *material_names,
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

group_names = list({
    "ExcludeAttachmentType",
    "KeywordsExcluded",
    "KeywordsIncluded",
    "KeywordsRequired",
    "Particle-ScaleAlongMovementVector",
    "SoundOnCreate",
    "SoundPersistent",
    "VoiceOverOnCreate",
    "VoiceOverPersistent",
    "dont-scroll-alpha-UV",
    "e-active",
    "e-alpharef",
    "e-beam-segments",
    "e-censor-policy",
    "e-disabled",
    "e-life",
    "e-life-scale",
    "e-linger",
    "e-local-orient",
    "e-period",
    "e-shape-name",
    "e-shape-scale",
    "e-shape-use-normal-for-birth",
    "e-soft-in-depth",
    "e-soft-out-depth",
    "e-soft-in-depth-delta",
    "e-soft-out-depth-delta",
    "e-timeoffset",
    "e-trail-cutoff",
    "e-uvscroll",
    "e-uvscroll-mult",
    "flag-brighter-in-fow",
    "flag-disable-z",
    "flag-force-animated-mesh-z-write",
    "flag-projected",
    *material_names,
    "p-alphaslicerange",
    "p-animation",
    "p-backfaceon",
    "p-beammode",
    "p-bindtoemitter",
    "p-coloroffset",
    "p-colorscale",
    "p-colortype",
    "p-distortion-mode",
    "p-distortion-power",
    "p-falloff-texture",
    "p-fixedorbit",
    "p-fixedorbittype",
    "p-flexoffset",
    "p-flexscale",
    "p-followterrain",
    "p-frameRate",
    "p-frameRate-mult",
    "p-fresnel",
    "p-life-scale",
    "p-life-scale-offset",
    "p-life-scale-symX",
    "p-life-scale-symY",
    "p-life-scale-symZ",
    "p-linger",
    "p-local-orient",
    "p-lockedtoemitter",
    "p-mesh",
    "p-meshtex",
    "p-meshtex-mult",
    "p-normal-map",
    "p-numframes",
    "p-numframes-mult",
    "p-offsetbyheight",
    "p-offsetbyradius",
    "p-orientation",
    "p-projection-fading",
    "p-projection-y-range",
    "p-randomstartframe",
    "p-randomstartframe-mult",
    "p-reflection-fresnel",
    "p-reflection-map",
    "p-reflection-opacity-direct",
    "p-reflection-opacity-glancing",
    "p-rgba",
    "p-scalebias",
    "p-scalebyheight",
    "p-scalebyradius",
    "p-scaleupfromorigin",
    "p-shadow",
    "p-simpleorient",
    "p-skeleton",
    "p-skin",
    "p-startframe",
    "p-startframe-mult",
    "p-texdiv",
    "p-texdiv-mult",
    "p-texture",
    "p-texture-mode",
    "p-texture-mult",
    "p-texture-mult-mode",
    "p-texture-pixelate",
    "p-trailmode",
    "p-type",
    "p-uvmode",
    "p-uvparallax-scale",
    "p-uvscroll-alpha-mult",
    "p-uvscroll-no-alpha",
    "p-uvscroll-rgb",
    "p-uvscroll-rgb-clamp",
    "p-uvscroll-rgb-clamp-mult",
    "p-vec-velocity-minscale",
    "p-vec-velocity-scale",
    "p-vecalign",
    "p-xquadrot-on",
    "pass",
    "rendermode",
    "single-particle",
    "submesh-list",
    "teamcolor-correction",
    "uniformscale",
    
    *flex_float(
        "p-scale", 
        "p-scaleEmitOffset",
    ),
    *flex_rand_float(
        "e-rate",
        "p-life",
        "p-rotvel",
    ),
    *flex_rand_vec2(
        "e-uvoffset",
    ),
    *flex_rand_vec3(
        "p-offset",
        "p-postoffset",
        "p-vel",
    ),
    *rand_color(
        "e-censor-modulate",
        "e-rgba",
        "p-fresnel-color",
        "p-reflection-fresnel-color",
        "p-xrgba",
    ),
    *rand_float(
        "e-color-modulate",
        "e-framerate",
        "p-bindtoemitter",
        "p-life",
        "p-quadrot",
        "p-rotvel",
        "p-scale",
        "p-xquadrot",
        "p-xscale",
        "e-rate",
    ),
    *rand_vec2(
        "e-ratebyvel",
        "e-uvoffset",
        "e-uvoffset-mult",
        "p-uvscroll-rgb",
        "p-uvscroll-rgb-mult",
    ),
    *rand_vec3(
        "Emitter-BirthRotationalAcceleration",
        "Particle-Acceleration",
        "Particle-Drag",
        "Particle-Velocity",
        "e-tilesize",
        "p-accel",
        "p-drag",
        "p-offset",
        "p-orbitvel",
        "p-postoffset",
        "p-quadrot",
        "p-rotvel",
        "p-scale",
        "p-vel",
        "p-worldaccel",
        "p-xquadrot",
        "p-xrgba-beam-bind-distance",
        "p-xscale",
    ),
    "ChildParticleName",
    "ChildSpawnAtBone",
    "ChildEmitOnDeath",
    "p-childProb",
    *[ name % x for name in [
            "ChildParticleName%d",
            "ChildSpawnAtBone%d",
            "ChildEmitOnDeath%d",
        ] for x in range(0, 10)
    ],

    *rand_float( *[ "e-rotation%d" % x for x in range(0,ROT_VARS) ] ),
    *[ "e-rotation%d-axis" % x for x in range(0,ROT_VARS) ],
    
    *part_field_names,
    *part_fluid_names,
})

fluid_names = [
    "f-accel",
    "f-buoyancy",
    "f-denseforce",
    "f-diffusion",
    "f-dissipation",
    "f-life",
    "f-initdensity",
    "f-movement-x",
    "f-movement-y",
    "f-viscosity",
    "f-startkick",
    "f-rate",
    "f-rendersize",
    *[ jet % x for jet in [
            "f-jetdir%u",
            "f-jetdirdiff%u",
            "f-jetpos%u",
            "f-jetspeed%u",
        ] for x in range(0, 4)
    ],
]

field_names = [
    "f-axisfrac",
    "f-localspace",
    *rand_float(
        "f-accel",
        "f-drag",
        "f-period",
        "f-radius",
        "f-veldelta",
    ),
    *rand_vec3(
        "f-accel",
        "f-direction",
        "f-pos",
    ),
]

def get_values(tbin, sections, names):
    vals = tbin["Values"]
    unks = tbin["UNKNOWN_HASHES"]
    for section, name, h in a_ihash(sections, names):
        if h in unks:
            yield unks[h]
        elif section in vals and name in vals[section]:
            yield vals[section][name]


def get_fixdict(tbin):
    if not "Values" in tbin:
        tbin["Values"] = {}
    if not "UNKNOWN_HASHES" in tbin:
        tbin["UNKNOWN_HASHES"] = {}
    groups = tuple(get_values(tbin, ["System"], part_group_names))
    fields = tuple(get_values(tbin, groups, part_field_names))
    fluids = tuple(get_values(tbin, groups, part_fluid_names))

    return {
        h : (s, n) for sn in [
            [ groups, group_names, ],
            [ fields, field_names, ],
            [ fluids, fluid_names, ],
            [ ["System"], system_names, ],
        ] for s,n,h in a_ihash(*sn)
    }

def fix(tbin, fixd = None):
    if fixd == None:
        fixd = get_fixdict(tbin)
    vals = tbin["Values"]
    unks = tbin["UNKNOWN_HASHES"]
    for h, (s, n) in fixd.items():
        if h in unks:
            if not s in vals:
                vals[s] = {}
            vals[s][n] = unks[h]
            del unks[h]
    
