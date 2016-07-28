package org.esa.snap.dataio.nc4;

import org.esa.snap.core.datamodel.Product;
import org.esa.snap.dataio.netcdf.ProfileWriteContext;
import org.esa.snap.dataio.netcdf.metadata.profiles.beam.BeamMetadataPart;

import java.io.IOException;

/**
 * Modification of BeamMetadataPart for CAWA purposes
 *
 * @author olafd
 */
public class SnapCawaMetadataPart extends BeamMetadataPart {
    @Override
    public void preEncode(ProfileWriteContext ctx, Product p) throws IOException {
        // nothing to do here for CAWA
    }
}
