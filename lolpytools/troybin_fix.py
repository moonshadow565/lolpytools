#!/usr/bin/env python
from sys import stderr
RAND_VARS=10
GPART_VARS=50
ROT_VARS=10
FIELD_VARS=10
COMMENTS=("%s", "'%s") 

def ihash(section, name):
    ret = 0
    for c in section + '*' + name:
        ret = (ord(c.lower()) +((65599 * ret) & 0xffffffff)) & 0xffffffff
    return ret

# flex('a') -> a_flex0, a_flex1, a_flex2, a_flex_3
def flex(*args):
    return ( "%s_flex%d" % (a,x) for a in args for x in range(0, 4) )

def rand(mods, *args):
    return (
        *args,
        *( "%s%u" % (a,x) for a in args for x in range(0, RAND_VARS) ),
        *( "%s%sP" % (a,m) for a in args for m in mods ),
        *( "%s%sP%u" % (a,m,x) for a in args for m in mods \
            for x in range(0, RAND_VARS)
        ),
    )

def rand_float(*args):
    return rand(('X', ''), *args)

def rand_vec2(*args):
    return rand(('X', 'Y'), *args)

def rand_vec3(*args):
    return rand(('X', 'Y', 'Z'), *args)

def rand_color(*args):
    return rand(('R', 'G', 'B', 'A'), *args)

def flex_rand_float(*args):
    return rand_float(*flex(*args))

def flex_rand_vec2(*args):
    return rand_vec2(*flex(*args))

def flex_rand_vec3(*args):
    return rand_vec3(*flex(*args))

def flex_rand_color(*args):
    return rand_color(*flex(*args))

material_names = (
    "MaterialOverrideTransMap",
    "MaterialOverrideTransSource",
    "p-trans-sample",
    *( mat % x for mat in (
        "MaterialOverride%dBlendMode",
        "MaterialOverride%dGlossTexture",
        "MaterialOverride%dEmissiveTexture",
        "MaterialOverride%dFixedAlphaScrolling",
        "MaterialOverride%dPriority",
        "MaterialOverride%dRenderingMode",
        "MaterialOverride%dSubMesh",
        "MaterialOverride%dTexture",
        "MaterialOverride%dUVScroll",
        ) for x in range(0,5) 
    ),
)

part_group_names = ( 
    *( "GroupPart%d" % x for x in range(0, GPART_VARS) ),
)

part_field_names = ( 
    *( field % x for field in (
            "field-accel-%d",
            "field-attract-%d",
            "field-drag-%d",
            "field-noise-%d",
            "field-orbit-%d",
        ) for x in range(1, FIELD_VARS)
    ),
)

part_fluid_names = (
    "fluid-params",
)

system_names = (
    "AudioFlexValueParameterName",
    "AudioParameterFlexID",
    "build-up-time",
    "group-vis",
    "group-scale-cap",
    *( g % x for g in (
        "GroupPart%d",
        "GroupPart%dType",
        "GroupPart%dImportance",
        "Override-Offset%d",
        "Override-Rotation%d",
        "Override-Scale%d",
        ) for x in range(0, GPART_VARS)
    ),
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
)

group_names = (
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
    
    *flex(
        "p-scale", 
        "p-scaleEmitOffset"
    ),
    *flex_rand_float(
        "e-rate",
        "p-life",
        "p-rotvel",
    ),
    *flex_rand_vec2(
        "e-uvoffset"
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
        "e-rate"
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
    *( name % x for name in (
            "ChildParticleName%d",
            "ChildSpawnAtBone%d",
            "ChildEmitOnDeath%d",
        ) for x in range(0, 10)
    ),

    *rand_float( *( "e-rotation%d" % x for x in range(0,ROT_VARS) ) ),
    *( "e-rotation%d-axis" % x for x in range(0,ROT_VARS) ),
    
    *part_field_names,
    *part_fluid_names,
)

fluid_names = (
    "f-viscosity",
    "f-diffusion",
    "f-accel",
    "f-buoyancy",
    "f-dissipation",
    "f-startkick",
    "f-denseforce",
    "f-movement-x",
    "f-movement-y",
    "f-initdensity",
    "f-life",
    "f-rate",
    "f-rendersize",
    *( jet % x for jet in (
            "f-jetpos%u",
            "f-jetdir%u",
            "f-jetspeed%u",
            "f-jetdirdiff%u",
        ) for x in range(0, 4)
    ),
)

field_names = (
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
        "f-accel"
        "f-direction"
        "f-pos",
    ),
)

def get_section(tbin, section, args):
    vals = tbin["Values"]
    unks = tbin["UNKNOWN_HASHES"]
    for a in args:
        for com in COMMENTS:
            name = com % a
            h = ihash(section, name)
            if section in vals and name in vals[section]:
                yield vals[section][name]
            elif h in unks:
                yield unks[h]

def fix_section(tbin, section, args):
    vals = tbin["Values"]
    unks = tbin["UNKNOWN_HASHES"]
    for a in args:
        for com in COMMENTS:
            name = com % a
            h = ihash(section, name)
            if h in unks:
                res = unks[h]
                if not section in vals:
                    vals[section] = {}
                vals[section][name] = res
                del unks[h]

def fix_dict(tbin):
    n_group = get_section(tbin, "System", part_group_names)
    return {
        **{ 
            ihash("System", n) : ("System", n) for n in system_names
        },
        **{
            ihash(g, n) : (g, n) for g in n_group \
                for n in group_names
        },
        **{
            ihash(s, n) : (s, n) for g in n_group \
                for s in get_section(tbin, g, part_field_names) \
                for n in field_names
        },
        **{
            ihash(s, n) : (s, n) for g in n_group \
                for s in get_section(tbin, g, part_fluid_names) \
                for n in fluid_names
        },
        **{
            ihash(s, n) : (s, n) for s, sects in tbin["Values"].items() \
                for n in sects
        },
    }

def fix(tbin):
    if not "Values" in tbin:
        tbin["Values"] = {}
    if not "UNKNOWN_HASHES" in tbin:
        tbin["UNKNOWN_HASHES"] = {}

    fix_section(tbin, "System", system_names)
    for group in get_section(tbin, "System", part_group_names):
        fix_section(tbin, group, group_names)
        
        for field in get_section(tbin, group, part_field_names):
            fix_section(tbin, field, field_names)
            
        for fluid in get_section(tbin, group, part_fluid_names):
            fix_section(tbin, fluid, fluid_names)


