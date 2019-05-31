#!/usr/bin/env python
from .inibin import ihash
from sys import stderr

system_fixlist = [
    "AudioFlexValueParameterName",
    "AudioParameterFlexID",
    "build-up-time",
    "group-vis",
    "group-scale-cap",
    "KeepOrientationAfterSpellCast",
    *[ mat.format(x) for x in range(0,5) for mat in [
            "MaterialOverride{}BlendMode",
            "MaterialOverride{}GlossTexture",
            "MaterialOverride{}EmissiveTexture",
            "MaterialOverride{}FixedAlphaScrolling",
            "MaterialOverride{}Priority",
            "MaterialOverride{}RenderingMode",
            "MaterialOverride{}SubMesh",
            "MaterialOverride{}Texture",
            "MaterialOverride{}UVScroll",
        ]
    ],
    "MaterialOverrideTransMap",
    "MaterialOverrideTransSource",
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

# TODO: impl Riot::ParticleSystem::AnimatedVariableWithRandomFactor<T>

def get_troy(tbin, section, name):
    get(tbin, section, name)
    for i in range(0, 10):
        get(tbin, section, "{}{}".format(name, i))
    return True

def get_prob(tbin, section, name):
    get(tbin, section, name)
    for i in range(0, 10):
        get(tbin, section, "{}{}".format(name, i))
    return True
    

def getr_vec3(tbin, section, name):
    if get_troy(tbin, section, name):
        for x in ['X','Y','Z']:
            get_prob(tbin, section, "{}{}P".format(name,x))

def getr_vec2(tbin, section, name):
    if get_troy(tbin, section, name):
        for x in ['X','Y']:
            get_prob(tbin, section, "{}{}P".format(name,x))

def getr_color(tbin, section, name):
    if get_troy(tbin, section, name):
        for x in ['R','G','B','A']:
            get_prob(tbin, section, "{}{}P".format(name,x))
    
def getr_float(tbin, section, name):
    if get_troy(tbin, section, name):
        get_prob(tbin, section, "{}XP".format(name))
        get_prob(tbin, section, "{}P".format(name))


# TODO: impl
# Riot::ParticleSystem::FlexType< 
#   Riot::ParticleSystem::AnimatedVariableWithRandomFactor<T>>
# and
# Riot::ParticleSystem::FlexType<float>
def getfr_vec3(tbin, section, name):
    for x in range(0, 4):
        getr_vec3(tbin, section, "{}_flex{}".format(name, x))

def getfr_vec2(tbin, section, name):
    for x in range(0, 4):
        getr_vec2(tbin, section, "{}_flex{}".format(name, x))

def getfr_color(tbin, section, name):
    for x in range(0, 4):
        getr_color(tbin, section, "{}_flex{}".format(name, x))

def getfr_float(tbin, section, name):
    for x in range(0, 4):
        getr_float(tbin, section, "{}_flex{}".format(name, x))

def getf_float(tbin, section, name):
    for x in range(0, 4):
        get(tbin, section, "{}_flex{}".format(name, x))



# TODO: add collision checking
def raw_get(tbin, section, name, defValue = None):
    if not "Values" in tbin:
        tbin["Values"] = {}
    if not "UNKNOWN_HASHES" in tbin:
        tbin["UNKNOWN_HASHES"] = {}
    vals = tbin["Values"]
    unks = tbin["UNKNOWN_HASHES"]
    if section in vals and name in vals[section]:
        return vals[section][name]
    h = ihash(section, name)
    if h in unks:
        res = unks[h]
        if not section in vals:
            vals[section] = {}
        vals[section][name] = res
        del unks[h]
        return res
    h = str(h)
    if h in unks:
        res = unks[h]
        if not section in vals:
            vals[section] = {}
        vals[section][name] = res
        del unks[h]
        return res
    return defValue

def get(tbin, section, name, defValue = None):
    raw_get(tbin, section, "'"+name, defValue)
    return raw_get(tbin, section, name, defValue)


def fix_simple(tbin, section):
    get(tbin, section, "rendermode")
    get(tbin, section, "pass")
    get(tbin, section, "e-alpharef")
    get(tbin, section, "p-uvmode")
    get(tbin, section, "p-distortion-power")
    get(tbin, section, "p-distortion-mode")
    get(tbin, section, "dont-scroll-alpha-UV")
    get(tbin, section, "p-uvscroll-no-alpha")
    get(tbin, section, "p-alphaslicerange")
    get(tbin, section, "flag-disable-z")
    get(tbin, section, "flag-projected")
    get(tbin, section, "flag-force-animated-mesh-z-write")
    get(tbin, section, "teamcolor-correction")
    get(tbin, section, "flag-brighter-in-fow")
    get(tbin, section, "p-texture")
    get(tbin, section, "p-texdiv")
    get(tbin, section, "p-rgba")
    get(tbin, section, "p-normal-map")
    get(tbin, section, "p-falloff-texture")
    get(tbin, section, "ExcludeAttachmentType")
    get(tbin, section, "KeywordsExcluded")
    get(tbin, section, "KeywordsRequired")
    get(tbin, section, "KeywordsIncluded")
    get(tbin, section, "p-texture-mode")
    get(tbin, section, "p-startframe")
    get(tbin, section, "p-numframes")
    get(tbin, section, "p-frameRate")
    get(tbin, section, "p-type")
    get(tbin, section, "p-skin")
    get(tbin, section, "p-animation")
    get(tbin, section, "p-mesh")
    get(tbin, section, "p-projection-y-range")
    get(tbin, section, "p-projection-fading")
    get(tbin, section, "p-backfaceon")
    get(tbin, section, "p-uvscroll-rgb")
    get(tbin, section, "p-uvscroll-rgb-clamp")
    get(tbin, section, "p-vecalign")
    get(tbin, section, "Particle-ScaleAlongMovementVector")
    getr_float(tbin, section, "p-xscale")
    getr_float(tbin, section, "p-xquadrot")
    get(tbin, section, "p-xquadrot-on")
    get(tbin, section, "e-timeoffset")
    get(tbin, section, "e-life")
    get(tbin, section, "e-life-scale")
    get(tbin, section, "e-active")
    get(tbin, section, "e-period")
    get(tbin, section, "p-shadow")
    get(tbin, section, "p-texture-pixelate")
    get(tbin, section, "single-particle")
    getfr_float(tbin, section, "e-rate")
    getr_float(tbin, section,"e-rate")
    getr_float(tbin, section, "p-life")
    getfr_float(tbin, section, "p-life")
    get(tbin, section, "p-life-scale")
    getr_vec3(tbin, section, "p-postoffset")
    getfr_vec3(tbin, section, "p-postoffset")
    getr_float(tbin, section, "p-quadrot")
    getr_float(tbin, section, "p-scale")
    getfr_vec3(tbin, section, "p-vel")
    getr_vec3(tbin, section, "p-vel")
    getr_float(tbin, section, "p-rotvel")
    getfr_float(tbin, section, "p-rotvel")
    get(tbin, section, "e-local-orient")
    get(tbin, section, "p-local-orient")
    get(tbin, section, "p-fixedorbit")
    get(tbin, section, "p-fixedorbittype")
    getr_vec3(tbin, section, "p-offset")
    get(tbin, section, "p-bindtoemitter")
    get(tbin, section, "p-lockedtoemitter")
    get(tbin, section, "p-followterrain")
    get(tbin, section, "p-scalebias")
    get(tbin, section, "p-simpleorient")
    get(tbin, section, "p-randomstartframe")
    get(tbin, section, "p-scaleupfromorigin")
    get(tbin, section, "p-colortype")
    get(tbin, section, "p-colorscale")
    get(tbin, section, "p-coloroffset")
    getr_float(tbin, section, "e-color-modulate")
    getr_color(tbin, section, "e-censor-modulate")
    get(tbin, section, "p-linger")
    get(tbin, section, "e-linger")
    get(tbin, section, "p-flexoffset")
    get(tbin, section, "p-flexscale")
    get(tbin, section, "p-offsetbyheight")
    get(tbin, section, "p-scalebyheight")
    get(tbin, section, "p-offsetbyradius")
    get(tbin, section, "p-scalebyradius")
    getf_float(tbin, section, "p-scaleEmitOffset")
    getf_float(tbin, section, "p-scale")
    getfr_vec3(tbin, section, "p-offset")
    get(tbin, section, "SoundOnCreate")
    get(tbin, section, "VoiceOverOnCreate")
    get(tbin, section, "SoundPersistent")
    get(tbin, section, "VoiceOverPersistent")

def fix_complex(tbin, section):
    get(tbin, section, "ExcludeAttachmentType")
    get(tbin, section, "KeywordsExcluded")
    get(tbin, section, "KeywordsRequired")
    get(tbin, section, "KeywordsIncluded")
    get(tbin, section, "p-texture-mode")
    get(tbin, section, "p-texture-mult-mode")
    get(tbin, section, "p-startframe")
    get(tbin, section, "p-startframe-mult")
    get(tbin, section, "p-numframes")
    get(tbin, section, "p-numframes-mult")
    get(tbin, section, "p-frameRate")
    get(tbin, section, "p-frameRate-mult")
    get(tbin, section, "p-type")
    get(tbin, section, "p-mesh")
    get(tbin, section, "p-skin")
    get(tbin, section, "p-meshtex")
    get(tbin, section, "p-meshtex-mult")
    get(tbin, section, "e-shape-name")
    get(tbin, section, "e-shape-scale")
    get(tbin, section, "e-shape-use-normal-for-birth")
    get(tbin, section, "p-animation")
    get(tbin, section, "p-projection-y-range")
    get(tbin, section, "p-projection-fading")
    get(tbin, section, "p-backfaceon")
    getr_vec2(tbin, section, "p-uvscroll-rgb")
    getr_vec2(tbin, section, "p-uvscroll-rgb-mult")
    get(tbin, section, "p-uvscroll-alpha-mult")
    get(tbin, section, "p-uvscroll-rgb-clamp")
    get(tbin, section, "p-uvscroll-rgb-clamp-mult")
    getr_vec3(tbin, section, "Particle-Velocity")
    getr_vec3(tbin, section, "Particle-Acceleration")
    getr_vec3(tbin, section, "p-worldaccel")
    getr_vec3(tbin, section, "p-xscale")
    getr_vec3(tbin, section, "p-xrgba-beam-bind-distance")
    getr_color(tbin, section, "p-xrgba")
    getr_float(tbin, section, "p-bindtoemitter")
    getr_vec3(tbin, section, "Particle-Drag")
    getr_vec3(tbin, section, "p-xquadrot")
    get(tbin, section, "p-xquadrot-on")
    get(tbin, section, "p-vecalign")
    get(tbin, section, "uniformscale")
    get(tbin, section, "p-vec-velocity-scale")
    get(tbin, section, "p-vec-velocity-minscale")
    get(tbin, section, "p-orientation")
    get(tbin, section, "p-local-orient")
    get(tbin, section, "p-randomstartframe")
    get(tbin, section, "p-randomstartframe-mult")
    get(tbin, section, "p-shadow")
    get(tbin, section, "p-distortion-power")
    get(tbin, section, "p-uvmode")
    get(tbin, section, "p-uvscroll-no-alpha")
    get(tbin, section, "p-uvparallax-scale")
    get(tbin, section, "p-trailmode")
    get(tbin, section, "p-beammode")
    get(tbin, section, "p-followterrain")
    get(tbin, section, "rendermode")
    get(tbin, section, "flag-disable-z")
    get(tbin, section, "flag-force-animated-mesh-z-write")
    get(tbin, section, "flag-projected")
    get(tbin, section, "teamcolor-correction")
    get(tbin, section, "flag-brighter-in-fow")
    get(tbin, section, "pass")
    get(tbin, section, "e-alpharef")
    get(tbin, section, "p-backfaceon")
    get(tbin, section, "p-texture")
    get(tbin, section, "p-texture-mult")
    get(tbin, section, "p-texdiv")
    get(tbin, section, "p-texdiv-mult")
    get(tbin, section, "p-rgba")
    get(tbin, section, "p-normal-map")
    get(tbin, section, "p-falloff-texture")
    get(tbin, section, "p-reflection-map")
    get(tbin, section, "p-reflection-opacity-direct")
    get(tbin, section, "p-reflection-opacity-glancing")
    get(tbin, section, "p-reflection-fresnel")
    getr_color(tbin, section, "p-reflection-fresnel-color")
    get(tbin, section, "p-fresnel")
    getr_color(tbin, section, "p-fresnel-color")
    get(tbin, section, "p-reflection-map")
    get(tbin, section, "e-timeoffset")
    get(tbin, section, "e-life")
    get(tbin, section, "e-life-scale")
    get(tbin, section, "e-active")
    get(tbin, section, "e-period")
    get(tbin, section, "e-trail-cutoff")
    get(tbin, section, "e-beam-segments")
    get(tbin, section, "single-particle")
    getr_float(tbin, section,"e-rate")
    getfr_float(tbin, section, "e-rate")
    getr_float(tbin, section, "p-life")
    getfr_float(tbin, section, "p-life")
    get(tbin, section, "p-life-scale")
    getr_vec2(tbin, section, "e-ratebyvel")
    get(tbin, section, "p-life-scale-offset")
    get(tbin, section, "p-life-scale-symX")
    get(tbin, section, "p-life-scale-symY")
    get(tbin, section, "p-life-scale-symZ")
    get(tbin, section, "p-distortion-power")
    get(tbin, section, "p-distortion-mode")
    get(tbin, section, "p-alphaslicerange")
    getr_vec3(tbin, section, "p-postoffset")
    getfr_vec3(tbin, section, "p-postoffset")
    getr_vec3(tbin, section, "p-quadrot")
    getr_vec3(tbin, section, "p-scale")
    getr_color(tbin, section, "e-rgba")
    getr_vec3(tbin, section, "p-vel")
    getr_vec3(tbin, section, "p-accel")
    getr_vec3(tbin, section, "p-rotvel")
    getr_vec3(tbin, section, "Emitter-BirthRotationalAcceleration")
    getr_vec3(tbin, section, "p-drag")
    getr_vec3(tbin, section, "p-orbitvel")
    getr_float(tbin, section, "e-framerate")
    get(tbin, section, "e-local-orient")
    get(tbin, section, "p-texture-pixelate")
    getr_vec3(tbin, section, "p-offset")
    get(tbin, section, "p-colortype")
    get(tbin, section, "p-colorscale")
    get(tbin, section, "p-coloroffset")
    getr_float(tbin, section, "e-color-modulate")
    getr_color(tbin, section, "e-censor-modulate")
    get(tbin, section, "p-linger")
    get(tbin, section, "e-linger")
    get(tbin, section, "p-flexoffset")
    get(tbin, section, "p-flexscale")
    get(tbin, section, "p-offsetbyheight")
    get(tbin, section, "p-scalebyheight")
    get(tbin, section, "p-offsetbyradius")
    get(tbin, section, "p-scalebyradius")
    getf_float(tbin, section, "p-scaleEmitOffset")
    getf_float(tbin, section, "p-scale")
    getfr_vec3(tbin, section, "p-offset")
    getfr_vec2(tbin, section, "e-uvoffset")
    getr_vec3(tbin, section, "e-tilesize")
    getr_vec2(tbin, section, "e-uvoffset")
    getr_vec2(tbin, section, "e-uvoffset-mult")
    get(tbin, section, "e-uvscroll")
    get(tbin, section, "e-uvscroll-mult")
    get(tbin, section, "SoundOnCreate")
    get(tbin, section, "VoiceOverOnCreate")
    get(tbin, section, "SoundPersistent")
    get(tbin, section, "VoiceOverPersistent")
    get(tbin, section, "submesh-list")
    
    get(tbin, section, "ChildParticleName")
    get(tbin, section, "ChildSpawnAtBone")
    get(tbin, section, "ChildEmitOnDeath")
    getr_float(tbin, section, "p-childProb")
    for x in range(0, 10):
        get(tbin, section, "ChildParticleName{}".format(x))
        get(tbin, section, "ChildSpawnAtBone{}".format(x))
        get(tbin, section, "ChildEmitOnDeath{}".format(x))

def fix_material(tbin, section):
    def hget(name, x):
        get(tbin, section, name.format(x), None)
    for x in range(0, 5):
        hget("MaterialOverride{}BlendMode", x)
        hget("MaterialOverride{}GlossTexture", x)
        hget("MaterialOverride{}EmissiveTexture", x)
        hget("MaterialOverride{}FixedAlphaScrolling", x)
        hget("MaterialOverride{}Priority", x)
        hget("MaterialOverride{}RenderingMode", x)
        hget("MaterialOverride{}SubMesh", x)
        hget("MaterialOverride{}Texture", x)
        hget("MaterialOverride{}UVScroll", x)

def fix_fluid(tbin, section):
    get(tbin, section, "f-viscosity")
    get(tbin, section, "f-diffusion")
    get(tbin, section, "f-accel")
    get(tbin, section, "f-buoyancy")
    get(tbin, section, "f-dissipation")
    get(tbin, section, "f-startkick")
    get(tbin, section, "f-denseforce")
    get(tbin, section, "f-movement-x")
    get(tbin, section, "f-movement-y")
    for x in range(1, 4):
        get(tbin, section, "f-jetpos%u" % x)
        get(tbin, section, "f-jetdir%u" % x)
        get(tbin, section, "f-jetspeed%u" % x)
        get(tbin, section, "f-jetdirdiff%u" % x)
    get(tbin, section, "f-initdensity")
    get(tbin, section, "f-life")
    get(tbin, section, "f-rate")
    get(tbin, section, "f-rendersize")

def fix_field_accel(tbin, accel):
    get(tbin, accel, "f-localspace")
    getr_vec3(tbin, accel, "f-accel")

def fix_field_attract(tbin, attract):
    getr_vec3(tbin, attract, "f-pos")
    getr_float(tbin, attract, "f-radius")
    getr_float(tbin, attract, "f-accel")
    
def fix_field_drag(tbin, drag):
    getr_vec3(tbin, drag, "f-pos")
    getr_float(tbin, drag, "f-radius")
    getr_float(tbin, drag, "f-drag")
    
def fix_field_noise(tbin, noise):
    getr_vec3(tbin, noise, "f-pos")
    getr_float(tbin, noise, "f-radius")
    getr_float(tbin, noise, "f-period")
    getr_float(tbin, noise, "f-veldelta")
    get(tbin, noise, "f-axisfrac")
    
def fix_field_orbit(tbin, orbit):
    get(tbin, orbit, "f-localspace")
    getr_vec3(tbin, orbit, "f-direction")

def fix_field_collection(tbin, section):
    for x in range(1, 10):
        accel = raw_get(tbin, section, "field-accel-%d" % x)
        if accel != None:
            fix_field_accel(tbin, accel)
        
        accel2 = raw_get(tbin, section, "'field-accel-%d" % x)
        if accel2 != None:
            fix_field_accel(tbin, accel2)
            
        attract = raw_get(tbin, section, "field-attract-%d" % x)
        if attract != None:
            fix_field_attract(tbin, attract)
        
        attract2 = raw_get(tbin, section, "'field-attract-%d" % x)
        if attract2 != None:
            fix_field_attract(tbin, attract2)
        
        drag = raw_get(tbin, section, "field-drag-%d" % x)
        if drag != None:
            fix_field_drag(tbin, drag)

        drag2 = raw_get(tbin, section, "'field-drag-%d" % x)
        if drag2 != None:
            fix_field_drag(tbin, drag2)

        noise = raw_get(tbin, section, "field-noise-%d" % x)
        if noise != None:
            fix_field_noise(tbin, noise)
            
        noise2 = raw_get(tbin, section, "'field-noise-%d" % x)
        if noise2 != None:
            fix_field_noise(tbin, noise2)

        orbit = raw_get(tbin, section, "field-orbit-%d" % x)
        if orbit != None:
            fix_field_orbit(tbin, orbit)

        orbit2 = raw_get(tbin, section, "'field-orbit-%d" % x)
        if orbit2 != None:
            fix_field_orbit(tbin, orbit2)

def fix_common(tbin, section):
    get(tbin, section, "e-disabled")
    get(tbin, section, "e-censor-policy")
    get(tbin, section, "p-skeleton")
    get(tbin, section, "e-soft-in-depth")
    get(tbin, section, "e-soft-out-depth")
    get(tbin, section, "e-soft-in-depth-delta")
    get(tbin, section, "e-soft-out-depth-delta")
    get(tbin, section, "MaterialOverrideTransMap")
    get(tbin, section, "p-trans-sample")
    get(tbin, section, "MaterialOverrideTransSource")

    fix_field_collection(tbin, section)
    fix_material(tbin, section)
    
    for x in range(1, 10):
        getr_float(tbin, section, "e-rotation{}".format(x))
        get(tbin, section, "e-rotation{}-axis".format(x))

    fluid = raw_get(tbin, section, "fluid-params")
    if fluid != None:
        fix_fluid(tbin, fluid)

    fluid2 = raw_get(tbin, section, "fluid-params")
    if fluid != None:
        fix_fluid(tbin, fluid2)



def fix_part(tbin, part, index, iscommented = False):
    fix_common(tbin, part)
    ptyp = get(tbin, "System", "GroupPart%dType" % index, "Complex")
    if iscommented or True:
        fix_simple(tbin, part)
        fix_complex(tbin, part)
        return
    if ptyp.lower() == "Simple".lower():
        fix_simple(tbin, part)
    else:
        fix_complex(tbin, part)

def fix(tbin):
    for name in system_fixlist:
        get(tbin, "System", name)
    index = 1
    fix_part(tbin, "System", 0, True)
    while True:
        get(tbin, "System", "GroupPart%dImportance" % index, "Medium")
        get(tbin, "System", "GroupPart%dType" % index, "Complex")
        get(tbin, "System", "Override-Offset%d" % index)
        get(tbin, "System", "Override-Rotation%d" % index)
        get(tbin, "System", "Override-Scale%d" % index)
        
        part = raw_get(tbin, "System", "GroupPart%d" % index)
        if part != None:
            fix_part(tbin, part, index)

        part2 = raw_get(tbin, "System", "'GroupPart%d" % index)
        if part2 != None:
            fix_part(tbin, part2, index, True)

        if part == None and part2 == None:
            if index > 50:
                break
        index += 1
