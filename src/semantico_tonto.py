def verificar_semantica(sintese):
    """
    Analisa a estrutura sintática coletada e valida os 6 padrões ODP do Tonto.
    Retorna:
    - padroes_identificados: Lista de strings descrevendo o que foi achado.
    - erros_semanticos: Lista de erros com sugestões de coerção.
    """
    
    classes = sintese["classes"]
    gensets = sintese["generalizacoes"]
    relacoes_externas = sintese["relacoes_externas"]
    
    padroes_identificados = []
    erros = []

    # =========================================================================
    # 1. SUBKIND PATTERN
    # Regra: Kind -> Subkind. Genset deve ser disjoint.
    # =========================================================================
    for g in gensets:
        general = g['general']
        specifics = g['specifics']
        modifiers = g['modifiers']
        
        # Verifica estereótipos
        gen_stereo = classes.get(general, {}).get('estereotipo')
        
        # Se o pai é Kind
        if gen_stereo == 'kind':
            # Verifica se todos os filhos são subkind
            all_subkinds = True
            for spec in specifics:
                spec_stereo = classes.get(spec, {}).get('estereotipo')
                # Ignora se for kind (erro de modelagem, mas foca no padrao)
                if spec_stereo != 'subkind' and spec_stereo != 'kind': 
                     if spec_stereo != 'subkind':
                         all_subkinds = False
            
            # Detecção do Padrão
            if all_subkinds and specifics:
                padrao_nome = f"Subkind Pattern ({general} -> {specifics})"
                
                if 'disjoint' in modifiers:
                    padroes_identificados.append(f"[OK] {padrao_nome}")
                else:
                    msg = f"Erro no {padrao_nome}: Genset '{g['nome']}' deve ser 'disjoint'."
                    coercao = f" -> Coerção: Assumindo 'disjoint' implicitamente para validar o padrão."
                    erros.append(msg + coercao)
                    padroes_identificados.append(f"[COERGIDO] {padrao_nome}")

    # =========================================================================
    # 2. ROLE PATTERN
    # Regra: Kind -> Role. Disjoint NÃO se aplica (não é obrigatório/comum).
    # =========================================================================
    for g in gensets:
        general = g['general']
        specifics = g['specifics']
        # modifiers = g['modifiers'] # Não usamos para validar erro aqui, pois é opcional
        gen_stereo = classes.get(general, {}).get('estereotipo')

        if gen_stereo == 'kind':
            # Verifica se filhos são role
            all_roles = True
            for spec in specifics:
                if classes.get(spec, {}).get('estereotipo') != 'role':
                    all_roles = False
            
            if all_roles and specifics:
                padrao_nome = f"Role Pattern ({general} -> {specifics})"
                padroes_identificados.append(f"[OK] {padrao_nome}")

    # =========================================================================
    # 3. PHASE PATTERN
    # Regra: Kind -> Phase. Disjoint é MANDATÓRIO.
    # =========================================================================
    for g in gensets:
        general = g['general']
        specifics = g['specifics']
        modifiers = g['modifiers']
        gen_stereo = classes.get(general, {}).get('estereotipo')

        if gen_stereo == 'kind':
            all_phases = True
            for spec in specifics:
                if classes.get(spec, {}).get('estereotipo') != 'phase':
                    all_phases = False
            
            if all_phases and specifics:
                padrao_nome = f"Phase Pattern ({general} -> {specifics})"
                if 'disjoint' in modifiers:
                    padroes_identificados.append(f"[OK] {padrao_nome}")
                else:
                    msg = f"Erro no {padrao_nome}: Genset '{g['nome']}' de fases DEVE ser 'disjoint'."
                    coercao = f" -> Coerção: Inserindo 'disjoint' no genset para prosseguir."
                    erros.append(msg + coercao)
                    padroes_identificados.append(f"[COERGIDO] {padrao_nome}")

    # =========================================================================
    # 4. RELATOR PATTERN
    # Relator --(mediation)--> Role --(specializes)--> Kind
    # E deve haver uma Material Relation conectando os Roles
    # =========================================================================
    relators = [name for name, data in classes.items() if data.get('estereotipo') == 'relator']
    
    for relator in relators:
        # Busca relações internas de mediação
        rels_internas = classes[relator].get('relacoes_internas', [])
        # Filtra as mediações. Formato parser: ('relacao_interna', {target, stereotypes, ...})
        mediations = []
        for r in rels_internas:
            dados = r[1]
            stereos = dados.get('stereotypes', [])
            # Normaliza esteriotipos (pode vir com @ ou sem)
            stereos_clean = [s.replace('@', '') for s in stereos if s]
            if 'mediation' in stereos_clean:
                mediations.append(dados['target'])
        
        # Validar alvos das mediações (Devem ser Roles)
        roles_envolvidos = []
        for target in mediations:
            t_stereo = classes.get(target, {}).get('estereotipo')
            if t_stereo == 'role':
                roles_envolvidos.append(target)
            else:
                msg = f"Erro no Relator Pattern '{relator}': Mediação aponta para '{target}' que é '{t_stereo}', esperava-se 'role'."
                coercao = f" -> Coerção: Tratando '{target}' como Role temporariamente."
                erros.append(msg + coercao)
                roles_envolvidos.append(target) # Coerção: aceita na lista para verificar o resto
        
        if len(roles_envolvidos) >= 2:
            # Verifica Material Relation entre os Roles
            has_material = False
            
            # Checa externas
            for rel_ext in relacoes_externas:
                # rel_ext é dict {source, target, stereotypes...}
                stereos = [s.replace('@', '') for s in rel_ext.get('stereotypes', []) if s]
                if 'material' in stereos:
                    # Verifica se conecta dois roles da lista
                    if rel_ext.get('source') in roles_envolvidos and rel_ext.get('target') in roles_envolvidos:
                        has_material = True
            
            padrao_nome = f"Relator Pattern ({relator} conecta {roles_envolvidos})"
            if has_material:
                padroes_identificados.append(f"[OK] {padrao_nome}")
            else:
                # Material relation é parte do padrão completo, mas às vezes implícita
                padroes_identificados.append(f"[AVISO] {padrao_nome}: Relação Material explícita entre os roles não encontrada.")

    # =========================================================================
    # 5. MODE PATTERN
    # Mode --(characterization)--> Kind
    # Mode --(externalDependence)--> Kind (outro)
    # =========================================================================
    modes = [name for name, data in classes.items() if data.get('estereotipo') == 'mode']
    
    for mode in modes:
        rels = classes[mode].get('relacoes_internas', [])
        has_charac = False
        has_ext_dep = False
        
        for r in rels:
            dados = r[1]
            stereos = [s.replace('@', '') for s in dados.get('stereotypes', []) if s]
            
            if 'characterization' in stereos:
                has_charac = True
            if 'externalDependence' in stereos:
                has_ext_dep = True
        
        padrao_nome = f"Mode Pattern ({mode})"
        if has_charac: 
            if has_ext_dep:
                padroes_identificados.append(f"[OK] {padrao_nome} completo.")
            else:
                msg = f"Padrão Mode '{mode}' incompleto: Falta @externalDependence."
                coercao = " -> Coerção: Marcando como Mode Pattern Parcial."
                erros.append(msg + coercao)
                padroes_identificados.append(f"[PARCIAL] {padrao_nome}")

    # =========================================================================
    # 6. ROLE MIXIN PATTERN
    # RoleMixin especializado por Roles. Roles especializam Kinds. 
    # Genset do RoleMixin deve ser disjoint e complete.
    # =========================================================================
    rolemixins = [name for name, data in classes.items() if data.get('estereotipo') == 'roleMixin']
    
    for rm in rolemixins:
        # Achar genset onde rm é o general
        genset_rm = None
        for g in gensets:
            if g['general'] == rm:
                genset_rm = g
                break
        
        if genset_rm:
            specifics = genset_rm['specifics']
            modifiers = genset_rm['modifiers']
            
            # Checa se specifics são Roles
            all_roles = True
            for spec in specifics:
                if classes.get(spec, {}).get('estereotipo') != 'role':
                    all_roles = False
            
            if all_roles:
                padrao_nome = f"RoleMixin Pattern ({rm} -> {specifics})"
                
                # Checa modificadores
                if 'disjoint' in modifiers and 'complete' in modifiers:
                    padroes_identificados.append(f"[OK] {padrao_nome}")
                else:
                    msg = f"Erro no {padrao_nome}: Genset de RoleMixin DEVE ser 'disjoint' e 'complete'."
                    coercao = f" -> Coerção: Assumindo {['disjoint', 'complete']} para validar."
                    erros.append(msg + coercao)
                    padroes_identificados.append(f"[COERGIDO] {padrao_nome}")

    return padroes_identificados, erros