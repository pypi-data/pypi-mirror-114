rule assign_lineage:
    input:
        fasta = os.path.join(IUPAC_CNS_FOLDER, "{sample}.iupac_consensus.fasta")
    output:
        os.path.join(DATAFOLDER["lineages"], "{sample}", "{sample}.lineage.txt")
    log:
        os.path.join(DATAFOLDER["logs"], "lineages", "{sample}.sort.log")
    params:
        dir = os.path.join(DATAFOLDER["lineages"], "{sample}"),
        fname = "{sample}.lineage.txt",
        pangolin_env= PANGOLIN
    conda:
        "../envs/conda.yaml"
    threads:
        10
    shell:
        r"""
            conda activate {params.pangolin_env} &> {log}
            pangolin --outdir {params.dir} --outfile {params.fname} --tempdir {params.dir} --threads {threads} {input.fasta} &>> {log}
        """

rule fuse_lineage:
    input:
        expand(os.path.join(DATAFOLDER["lineages"], "{sample}",
               "{sample}.lineage.txt"), sample=SAMPLES)
    output:
        os.path.join(DATAFOLDER["lineages"], "all_samples.lineage.txt")
    shell:
        r"""
        head -n1 {input[0]} > {output}
        ls -1 {input} | xargs -I '{{}}' tail -n +2 {{}} >> {output}
        """
